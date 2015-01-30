var page = require('webpage').create();
page.settings.userAgent = 'WebKit/534.46 Mobile/9A405 Safari/7534.48.3';
page.settings.viewportSize = { width: 400, height: 600 };
page.open('http://www.yooli.com/yuexitong/page/1.html', function (status) {
    if (status !== 'success') {
        console.log('Unable to load BBC!');
        phantom.exit();
    } else {	
        window.setTimeout(function () {
			console.log(page.content);
            phantom.exit();
        }, 2000);
    }
});
