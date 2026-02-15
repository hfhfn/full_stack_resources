Action()
{
	// 获取当前时间
	// lr_output_message("当前时间是%s", lr_eval_string("{time}"));

	//web_save_timestamp_param("time", LAST);
	// 1932374587367.34576

	// lr_output_message("当前时间是%s", lr_eval_string("{time}"));

	// 随机数
	lr_output_message(lr_eval_string("{random}"));
	return 0;
}
