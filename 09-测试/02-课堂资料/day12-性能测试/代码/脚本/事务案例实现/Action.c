Action()
{    
    // 注意变量必须定义 在开头
    int result;

    lr_start_transaction("登录");

    // 关联 session
    web_reg_save_param("Session",
        "LB=name=userSession value=",
        "RB=>",
        LAST);

    // 打开URL
    web_submit_data("web_submit_data",
        "Action=http://127.0.0.1:1080/WebTours/",
        "Method=GET",
        "TargetFrame=",
        "Referer=",
        "Mode=HTML",
        ITEMDATA,
        LAST);

    // 获取登录后的用户名
    web_reg_save_param("username",
        "LB=Welcome, <b>",
        "RB=</b>,",
        LAST);

    // 登录
    web_submit_data("登录",
        "Action=http://127.0.0.1:1080/WebTours/login.pl",
        "Method=POST",
        "TargetFrame=",    
        "Referer=",
        "Mode=HTML",
        ITEMDATA,
        "Name=userSession", "Value={Session}", ENDITEM,
        "Name=username", "Value=admin123", ENDITEM,
        "Name=password", "Value=12345678", ENDITEM,
        LAST);

    // 判断登录用户是否为jojo 0:为相等  ASCII码
    result = strcmp(lr_eval_string("{username}"),"jojo");
    if(result==0){
        lr_end_transaction("登录", LR_PASS);
        lr_output_message("结果为：%d,通过啦！",result);
    }else{
        lr_end_transaction("登录", LR_FAIL);
        lr_output_message("结果为：%d,错误啦！",result);
    }

    return 0;
}

