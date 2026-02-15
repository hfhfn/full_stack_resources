Action()
{
	// 需求: 20用户同时订票，登录在3s内完成，订票在15秒内完成；

	//设置关联
	

	web_reg_save_param("session",
		"LB=userSession value=",
		"RB=>",
		"NotFound=ERROR",
		"Search=All",
		LAST);


	// 打开登录页面
	web_url("web_url",
		"URL=http://127.0.0.1:1080/WebTours/",
		"TargetFrame=",
		"Resource=0",
		"Referer=",
		"Mode=HTML",
		LAST);

	// 登录
	// 要进行关联和参数化

	// 插入开始事务
    
	lr_start_transaction("login");



    // 插入集合点
    lr_rendezvous("登录");

	web_submit_data("web_submit_data",
		"Action=http://127.0.0.1:1080/WebTours/login.pl",
		"Method=POST",
		"TargetFrame=",
		"Referer=",
		"Mode=HTML",
		ITEMDATA,
		"Name=userSession", "Value={session}", ENDITEM,
		"Name=username", "Value={user_name}", ENDITEM,
		"Name=password", "Value={password}", ENDITEM,
		"Name=login.x", "Value=56", ENDITEM,
		"Name=login.y", "Value=4", ENDITEM,
		"Name=JSFormSubmit", "Value=on", ENDITEM,
		LAST);
    // 插入结束的事务
	lr_end_transaction("login", LR_AUTO);

	// 插入订票开始事务
	lr_start_transaction("订票");


	// 订票页面
	web_url("订票页面", "URL=http://127.0.0.1:1080/WebTours/welcome.pl?page=search",LAST);

	// 选择航班
	web_submit_data("选择航班",
		"Action=http://localhost:1080/webtours/reservations.pl",
		"Method=POST",
		"TargetFrame=",
		"Referer=",
		ITEMDATA,
		"Name=.cgifields", "Value=roundtrip", ENDITEM,
		"Name=.cgifields", "Value=seatType", ENDITEM,
		"Name=.cgifields", "Value=seatPref", ENDITEM,
		"Name=advanceDiscount", "Value=0", ENDITEM,
		"Name=arrive", "Value=Denver", ENDITEM,
		"Name=depart", "Value=London", ENDITEM,
		"Name=departDate", "Value=12/29/2018", ENDITEM,
		"Name=findFlights.x", "Value=29", ENDITEM,
		"Name=findFlights.y", "Value=8", ENDITEM,
		"Name=numPassengers", "Value=1", ENDITEM,
		"Name=returnDate", "Value=12/30/2018", ENDITEM,
		"Name=seatPref", "Value=None", ENDITEM,
		"Name=seatType", "Value=Coach", ENDITEM,
		LAST);

    // 选择位置
	web_submit_data("座位",
		"Action=http://localhost:1080/webtours/reservations.pl",
		"Method=POST",
		"TargetFrame=",
		"Referer=",
		ITEMDATA,
		"Name=advanceDiscount", "Value=0", ENDITEM,
		"Name=numPassengers", "Value=1", ENDITEM,
		"Name=outboundFlight", "Value=200;338;12/29/2018", ENDITEM,
		"Name=reserveFlights.x", "Value=31", ENDITEM,
		"Name=reserveFlights.y", "Value=4", ENDITEM,
		"Name=seatPref", "Value=None", ENDITEM,
		"Name=seatType", "Value=Coach", ENDITEM,
		LAST);

    //付款信息

	web_submit_data("付款信息",
		"Action=http://localhost:1080/webtours/reservations.pl",
		"Method=POST",
		"TargetFrame=",
		"Referer=",
		ITEMDATA,
		"Name=JSFormSubmit", "Value=off", ENDITEM,
		"Name=address1", "Value=234 Willow Drive", ENDITEM,
		"Name=address2", "Value=San Jose/CA/94085", ENDITEM,
		"Name=.cgifields", "Value=saveCC", ENDITEM,
		"Name=advanceDiscount", "Value=0", ENDITEM,
		"Name=buyFlights.x", "Value=28", ENDITEM,
		"Name=buyFlights.y", "Value=12", ENDITEM,
		"Name=firstName", "Value=Joseph", ENDITEM,
		"Name=lastName", "Value=Marshall", ENDITEM,
		"Name=numPassengers", "Value=1", ENDITEM,
		"Name=outboundFlight", "Value=200;338;12/29/2018", ENDITEM,
		"Name=pass1", "Value=Joseph Marshall", ENDITEM,
		"Name=seatPref", "Value=None", ENDITEM,
		"Name=seatType", "Value=Coach", ENDITEM,
		LAST);

    // 插入订票结束事务
	lr_end_transaction("订票", LR_AUTO);

	// 退出

	web_url("退出", "URL=http://127.0.0.1:1080/WebTours/welcome.pl?signOff=1",LAST);

	return 0;
}
