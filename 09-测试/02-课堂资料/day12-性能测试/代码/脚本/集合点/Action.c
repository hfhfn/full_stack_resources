Action()
{

	web_set_max_html_param_len("1024");

	/* Registering parameter(s) from source task id 13
	// {WCSParam3} = "126266.186958283ztQtiVzpQQVzzzzHDiQzipQAVQf"
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

	lr_think_time(6);

	// 插入集合点
	lr_rendezvous("登录");

    // 插入开始事务
	lr_start_transaction("login");


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
		"Name=login.x", "Value=27", ENDITEM, 
		"Name=login.y", "Value=14", ENDITEM, 
		LAST);

	// 插入结束事务
	lr_end_transaction("login", LR_AUTO);


	return 0;
}