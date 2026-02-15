Action()
{
	// web_submit_data实现get方法
	web_submit_data("打开登录页面",
		"Action=http://127.0.0.1:1080/WebTours/",
		"Method=GET",
		"TargetFrame=",
		"Referer=",
		"Mode=HTML",
		ITEMDATA,
		LAST);

	// web_submit_data实现post方法
	web_submit_data("web_submit_data",
		"Action=http://127.0.0.1:1080/WebTours/login.pl",
		"Method=POST",
		"TargetFrame=",
		"Referer=",
		"Mode=HTML",
		ITEMDATA,
		"Name=userSession", "Value=126258.872742001ztQtttApHzzzzzzHDiQzzpzttz", ENDITEM,
		"Name=username", "Value=jojo", ENDITEM,
		"Name=password", "Value=bean", ENDITEM,
		"Name=login.x", "Value=47", ENDITEM,
		"Name=login.y", "Value=12", ENDITEM,
		"Name=JSFormSubmit", "Value=on", ENDITEM,
		LAST);

	// 退出
	web_custom_request("退出",
		"URL=http://127.0.0.1:1080/WebTours/welcome.pl?signOff=1",
		"Method=GET",
		"TargetFrame=",
		"Resource=1",
		"Referer=",
		"Mode=HTML",
		"Body=signOff=1",
		LAST);

	
	return 0;
}
