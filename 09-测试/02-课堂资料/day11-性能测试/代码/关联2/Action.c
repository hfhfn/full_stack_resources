Action()
{
	/*
    web_set_max_html_param_len("1024");
	// 手动关联

	// 注册函数,必须要卸载调用的函数前
	

	web_reg_save_param("login",
		"LB=<b>",
		"RB=</b>",
		"NotFound=ERROR",
		"Search=All",
		LAST);

	web_url("打开登录页面", "URL=http://127.0.0.1:1080/WebTours/", LAST);
	
	web_url("web_url",
		"URL=http://127.0.0.1:1080/WebTours/",
		"TargetFrame=",
		"Resource=0",
		"Referer=",
		"Mode=HTML",
		LAST);
	

	// 输出关联值
	lr_output_message("匹配的是%s", lr_eval_string("{login}"));

	*/
	//关联函数
	web_reg_save_param("WCSParam3", 
		"LB/IC=name=userSession value=", 
		"RB/IC=>", 
		"Ord=1", 
		"Search=Body", 
		"RelFrameId=1.2.1", 
		LAST);

	web_url("登录页面",
		"URL=http://127.0.0.1:1080/WebTours/",
		"TargetFrame=",
		"Resource=0",
		"Referer=",
		"Mode=HTML",
		LAST);

	// 登录函数
	web_submit_data("web_submit_data",
		"Action=http://127.0.0.1:1080/WebTours/login.pl",
		"Method=POST",
		"TargetFrame=",
		"Referer=",
		"Mode=HTML",
		ITEMDATA,
		"Name=username", "Value=jojo", ENDITEM,
		"Name=password", "Value=bean", ENDITEM,
		"Name=userSession", "Value={WCSParam3}", ENDITEM,
		"Name=login.x", "Value=47", ENDITEM,
		"Name=login.y", "Value=12", ENDITEM,
		"Name=JSFormSubmit", "Value=on", ENDITEM, 
		LAST);

	

	return 0;


}
