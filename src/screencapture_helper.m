#import <Cocoa/Cocoa.h>
#include <sandbox.h>
#import <ScreenCaptureKit/ScreenCaptureKit.h>
#import <ImageIO/ImageIO.h>
#import <UniformTypeIdentifiers/UniformTypeIdentifiers.h>

static NSString *gOutputPath = nil;
static NSString *gStatusPath = nil;

void writeStatus(NSString *message) {
    if (gStatusPath) {
        [message writeToFile:gStatusPath atomically:YES encoding:NSUTF8StringEncoding error:nil];
    }
    fprintf(stderr, "%s\n", message.UTF8String);
}

@interface AppDelegate : NSObject <NSApplicationDelegate>
@property (nonatomic) BOOL captureInProgress;
@end

@implementation AppDelegate

- (NSApplicationTerminateReply)applicationShouldTerminate:(NSApplication *)sender {
    // キャプチャ中は終了を拒否
    if (self.captureInProgress) {
        return NSTerminateCancel;
    }
    return NSTerminateNow;
}

- (void)applicationDidFinishLaunching:(NSNotification *)notification {
    self.captureInProgress = YES;

    NSString *bundlePath = [[NSBundle mainBundle] bundlePath];
    NSString *projectRoot = [bundlePath stringByDeletingLastPathComponent];
    NSString *configPath = [projectRoot stringByAppendingPathComponent:@"tmp/screencapture_config.txt"];

    // ステータスファイルパス
    gStatusPath = [projectRoot stringByAppendingPathComponent:@"tmp/screencapture_status.txt"];
    writeStatus(@"starting");

    NSError *readError = nil;
    gOutputPath = [[NSString stringWithContentsOfFile:configPath encoding:NSUTF8StringEncoding error:&readError]
                   stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceAndNewlineCharacterSet]];

    if (readError || !gOutputPath || gOutputPath.length == 0) {
        writeStatus([NSString stringWithFormat:@"error: config read failed: %@", configPath]);
        self.captureInProgress = NO;
        [NSApp terminate:nil];
        return;
    }

    writeStatus(@"fetching shareable content");

    [SCShareableContent getShareableContentWithCompletionHandler:^(SCShareableContent *content, NSError *error) {
        if (error || !content) {
            writeStatus([NSString stringWithFormat:@"error: %@", error.localizedDescription]);
            self.captureInProgress = NO;
            dispatch_async(dispatch_get_main_queue(), ^{ [NSApp terminate:nil]; });
            return;
        }

        writeStatus([NSString stringWithFormat:@"found %lu displays", (unsigned long)content.displays.count]);

        if (content.displays.count == 0) {
            writeStatus(@"error: no display found");
            self.captureInProgress = NO;
            dispatch_async(dispatch_get_main_queue(), ^{ [NSApp terminate:nil]; });
            return;
        }

        // マウスカーソルのあるディスプレイを探す。見つからなければ最初のディスプレイを使用
        CGEventRef event = CGEventCreate(NULL);
        CGPoint cursor = CGEventGetLocation(event);
        CFRelease(event);

        SCDisplay *targetDisplay = content.displays.firstObject;
        for (SCDisplay *display in content.displays) {
            if (CGRectContainsPoint(display.frame, cursor)) {
                targetDisplay = display;
                break;
            }
        }

        writeStatus([NSString stringWithFormat:@"capturing display %ux%u", (unsigned)targetDisplay.width, (unsigned)targetDisplay.height]);

        SCContentFilter *filter = [[SCContentFilter alloc] initWithDisplay:targetDisplay excludingWindows:@[]];
        SCStreamConfiguration *config = [[SCStreamConfiguration alloc] init];
        config.width = (size_t)(targetDisplay.width * 2);
        config.height = (size_t)(targetDisplay.height * 2);

        [SCScreenshotManager captureImageWithFilter:filter
                                      configuration:config
                                  completionHandler:^(CGImageRef image, NSError *captureError) {
            if (captureError || !image) {
                writeStatus([NSString stringWithFormat:@"error: capture failed: %@", captureError.localizedDescription]);
            } else {
                NSURL *url = [NSURL fileURLWithPath:gOutputPath];
                CGImageDestinationRef dest = CGImageDestinationCreateWithURL(
                    (__bridge CFURLRef)url,
                    (__bridge CFStringRef)UTTypePNG.identifier,
                    1, NULL);
                if (dest) {
                    CGImageDestinationAddImage(dest, image, NULL);
                    if (CGImageDestinationFinalize(dest)) {
                        writeStatus(@"ok");
                    } else {
                        writeStatus(@"error: failed to write PNG");
                    }
                    CFRelease(dest);
                } else {
                    writeStatus(@"error: failed to create image destination");
                }
            }
            self.captureInProgress = NO;
            dispatch_async(dispatch_get_main_queue(), ^{ [NSApp terminate:nil]; });
        }];
    }];
}

@end

int main(int argc, const char *argv[]) {
    @autoreleasepool {
        // --- 自己制限: ネットワーク・プロセス起動・シェル実行を禁止 ---
        // このアプリはスクショ撮影とtmp/への書き込みしかできない
        #include <sys/resource.h>
        struct rlimit nofile = {256, 256};  // FD数を最小限に制限
        setrlimit(RLIMIT_NOFILE, &nofile);

        // ネットワークソケット作成を禁止（sandbox_init は非推奨だがアプリ内自己適用は安全）
        #pragma clang diagnostic push
        #pragma clang diagnostic ignored "-Wdeprecated-declarations"
        char *sandbox_error = NULL;
        const char *profile =
            "(version 1)"
            "(allow default)"
            "(deny network*)";              // 全ネットワーク通信を禁止
        sandbox_init(profile, 0, &sandbox_error);
        if (sandbox_error) {
            fprintf(stderr, "sandbox warning: %s\n", sandbox_error);
            sandbox_free_error(sandbox_error);
        }
        #pragma clang diagnostic pop

        NSApplication *app = [NSApplication sharedApplication];
        [app setActivationPolicy:NSApplicationActivationPolicyAccessory];

        // 自動終了を無効化
        [[NSProcessInfo processInfo] disableAutomaticTermination:@"capture in progress"];

        AppDelegate *delegate = [[AppDelegate alloc] init];
        app.delegate = delegate;
        [app run];
        return 0;
    }
}
