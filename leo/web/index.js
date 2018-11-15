//@+leo-ver=5-thin
//@+node:pimgeek.20181115144950.1: * @file web/index.js
//@@language javascript

// 把下方的前端方法暴露给后端
eel.expose(py_to_js);
function py_to_js(py_param, is_over) {
	console.log("[js] py_to_js 方法：" + py_param);
	if (is_over === 'Y') {
		return 0;
	} else {
		eel.js_to_py("py_to_js 方法已经被后端调用了。", "Y");
	}
	return "py_to_js 工作正常！";
}

py_to_js("本方法在前端工作正常。","Y");

function confirm_py_call(msg) {
	console.log("[js] 已完成 js_to_py 方法在前端的调用。[" + msg + "]");
}

// 调用后端的方法
eel.js_to_py("前端已向后端发起 js_to_py 方法调用，收到后请用 py_to_js 回复！", "N")(confirm_py_call);
//@-leo
