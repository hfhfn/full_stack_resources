Action()
{

	web_set_max_html_param_len("1024");

	/* Registering parameter(s) from source task id 13
	// {WCSParam3} = "126258.685945727ztQttDVpVfiDDDDDDiQzzpfizQf"
	// */
	//获取sesion, 进行关联
	// 注册函数
	web_reg_save_param("WCSParam3", 
		"LB/IC=name=userSession value=", 
		"RB/IC=>", 
		"Ord=1", 
		"Search=Body", 
		"RelFrameId=1.2.1", 
		LAST);
/*
发起请求, get
	web_url("WebTours", 
		"URL=http://127.0.0.1:1080/WebTours/", 
		"Resource=0", 
		"RecContentType=text/html", 
		"Referer=", 
		"Snapshot=t1.inf", 
		"Mode=HTML", 
		LAST);


*/



	//发起请求, get
	web_url("WebTours", 
		"URL=http://127.0.0.1:1080/WebTours/", 
		"Resource=0", 
		"RecContentType=text/html", 
		"Referer=", 
		"Snapshot=t1.inf", 
		"Mode=HTML", 
		LAST);

	lr_think_time(12);

	web_submit_data("login.pl", 
		"Action=http://127.0.0.1:1080/WebTours/login.pl", 
		"Method=POST", 
		"RecContentType=text/html", 
		"Referer=http://127.0.0.1:1080/WebTours/nav.pl?in=home", 
		"Snapshot=t2.inf", 
		"Mode=HTML", 
		ITEMDATA, 
		"Name=userSession", "Value={WCSParam3}", ENDITEM, 
		"Name=username", "Value=jojo", ENDITEM, 
		"Name=password", "Value=bean", ENDITEM, 
		"Name=JSFormSubmit", "Value=on", ENDITEM, 
		"Name=login.x", "Value=56", ENDITEM, 
		"Name=login.y", "Value=10", ENDITEM, 
		LAST);

	lr_think_time(10);

	web_image("SignOff Button", 
		"Alt=SignOff Button", 
		"Snapshot=t3.inf", 
		LAST);

	return 0;
}