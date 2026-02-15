Action()
{
	// 实现登录网站

	//使用函数助手实现函数
	/*
	web_url("web_url",
		"URL=http://127.0.0.1:1080/WebTours/",
		"TargetFrame=",
		"Resource=0",
		"Referer=",
		"Mode=HTML",
		LAST);
	*/


	// 注册函数,先不用理解这个函数,先直接使用
	web_reg_save_param("session", 
		"LB/IC=name=userSession value=", 
		"RB/IC=>", 
		"Ord=1", 
		"Search=Body", 
		"RelFrameId=1.2.1", 
		LAST);


	// 纯手写
	web_url("打开登录页面",
			"URL=http://127.0.0.1:1080/WebTours/",
			LAST);

	// 实现登录

	web_submit_data("web_submit_data",
		"Action=http://127.0.0.1:1080/WebTours/login.pl",
		"Method=POST",
		"TargetFrame=",
		"Referer=",
		"Mode=HTML",
		ITEMDATA,
		"Name=userSession", "Value={session}", ENDITEM,
		"Name=password", "Value=bean", ENDITEM,
		"Name=login.x", "Value=47", ENDITEM,
		"Name=username", "Value=jojo", ENDITEM,
		"Name=login.y", "Value=12", ENDITEM,
		"Name=JSFormSubmit", "Value=on", ENDITEM,
		LAST);

	/*
	// 纯手写, 识别不了参数的格式
	web_submit_data("登录",
					"Action=http://127.0.0.1:1080/WebTours/login.pl",
					"Method=POST",
					ITEMDATA,
					"username=jojo",
					"password=bean",
					"login.x=47",
					"login.y=12",
					"JSFormSubmit=on",
					"usersession={session}",
					LAST);
*/


	return 0;
}
