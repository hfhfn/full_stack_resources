Action()
{

	web_set_max_html_param_len("1024");

	/* Registering parameter(s) from source task id 13
	// {WCSParam3} = "126265.729445119ztQtHQDptfiDDDDDDiQzipHzAHf"
	// */

	// 设置关联
	web_reg_save_param("WCSParam3", 
		"LB/IC=name=userSession value=", 
		"RB/IC=>", 
		"Ord=1", 
		"Search=Body", 
		"RelFrameId=1.2.1", 
		LAST);

	// 打开登录的页面
	web_url("WebTours", 
		"URL=http://127.0.0.1:1080/WebTours/", 
		"Resource=0", 
		"RecContentType=text/html", 
		"Referer=", 
		"Snapshot=t1.inf", 
		"Mode=HTML", 
		LAST);

	// 插入开始的事务
	lr_start_transaction("login");

	lr_think_time(57);

	// 登录的函数
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
		"Name=login.x", "Value=72", ENDITEM, 
		"Name=login.y", "Value=9", ENDITEM, 
		LAST);
	// 结束事务的时间
	lr_end_transaction("login",LR_AUTO);

	lr_think_time(28);

	web_image("SignOff Button", 
		"Alt=SignOff Button", 
		"Snapshot=t3.inf", 
		LAST);

	return 0;
}