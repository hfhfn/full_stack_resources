Action()
{
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

	


	// 注册函数
	// 设置检查点, 从内存查找
	/*
	web_reg_find("Fail=NotFound",
		"Search=Body",
		"SaveCount=1",
		"Text=jojo",
		LAST);
	*/
	


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

	// 必须放在请求后面
	web_find("check",
		"What=jojo",
		LAST);

	return 0;
}
