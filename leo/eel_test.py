# -*- coding: utf-8 -*-
#@+leo-ver=5-thin
#@+node:pimgeek.20181113171208.1: * @file eel_test.py
#@@first
#@@language python

import eel

# 指定包含前端代码的文件夹
eel.init('web')

# 把下方的 python 方法暴露给前端（以便 javascript 调用）
# 发生前端调用时，可以顺带接收到来自前端的数据（即方法参数）
@eel.expose	
def js_to_py(js_param, is_over):
		print('[py] js_to_py 方法：%s' % js_param)
		if (is_over == "Y"):
			pass
		else:
				eel.py_to_js("js_to_py 方法已经被前端调用了。", "Y");
		return "js_to_py 工作正常！"

# 直接在后端调用 python 方法
js_to_py('本方法在后端工作正常。','Y')

# 后端专用回调方法，可以获得方法的返回值
def confirm_backend_call_ended(msg):
		print("[py] 已完成 py_to_js 方法在后端的调用。[返回值 = %s]" % msg)

# 调用由前端暴露给后端的方法（对应一个 javascript 方法）
# 在后端调用时，可以顺带把后端数据作为参数发送给前端
eel.py_to_js('后端已向前端发起 py_to_js 方法调用，收到后请用 js_to_py 回复！','N')(confirm_backend_call_ended)

# 设置 eel 启动参数
my_start_urls = { 
		'scheme':'http',
		'host':'localhost',
		'port':8000,
		'path':'index.html'
		}
my_options = {
		'host':'0.0.0.0'
		}
# 启动 eel 服务
eel.start(
		my_start_urls,
		size=(800,600), 
		options=my_options
		)
#@-leo
