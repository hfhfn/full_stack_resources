Action()
{

	web_set_max_html_param_len("1024");

	/* Registering parameter(s) from source task id 13
	// {WCSParam3} = "126265.850870798ztQtHQQpHAtVzzzHDiQzipHQiccf"
	// */

	web_reg_save_param("WCSParam3", 
		"LB/IC=name=userSession value=", 
		"RB/IC=>", 
		"Ord=1", 
		"Search=Body", 
		"RelFrameId=1.2.1", 
		LAST);

	web_url("WebTours", 
		"URL=http://127.0.0.1:1080/WebTours/", 
		"Resource=0", 
		"RecContentType=text/html", 
		"Referer=", 
		"Snapshot=t1.inf", 
		"Mode=HTML", 
		LAST);

	lr_think_time(7);

	// 插入开始事务
	
	lr_start_transaction("登录");


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
		"Name=login.x", "Value=50", ENDITEM, 
		"Name=login.y", "Value=14", ENDITEM, 
		LAST);

	// 插入结束的事务
	lr_end_transaction("登录", LR_AUTO);

	web_image("SignOff Button", 
		"Alt=SignOff Button", 
		"Snapshot=t3.inf", 
		LAST);

	return 0;
}