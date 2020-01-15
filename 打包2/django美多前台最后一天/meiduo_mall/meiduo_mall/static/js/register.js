// 创建vue对象
let vm = new Vue({
    el: '#app',// 通过id选择器找到绑定的html内容
    // 修改Vue读取变量的语法
    delimiters: ['[[', ']]'],
    data: {//数据对象
        //v-model
        username: '',
        password: '',
        password2: '',
        mobile: '',
        allow: '',
        image_code_url: '',
        uuid: '',
        image_code: '',
        sms_code: '',

        //v-show
        error_name: false,
        error_password: false,
        error_password2: false,
        error_mobile: false,
        error_allow: false,
        error_image_code: false,
        error_sms_code: false,

        //error_message
        error_name_message: '',
        error_mobile_message: '',
        error_image_code_message: '',
        error_sms_code_message: '',
        sms_code_tip: '获取短信验证码',
        send_flag: false,
    },
    mounted(){//页面加载完调用
        // 生成图形验证码
        this.generate_image_code();
    },
    methods: {// 定义和实现事件的方法
        //生成图形验证码方法,封装的实现，方便代码复用
        generate_image_code(){
            this.uuid = generateUUID();
            this.image_code_url = '/image_codes/' + this.uuid + '/';
        },

        //发送手机验证码
        send_sms_code(){
            // 避免频繁点击获取验证码
            if (this.send_flag == true) { //先判断时候有人在上厕所,true代表关门了
                return;  //有人在厕所 退回去
            }
            this.send_flag = true; //如果可以进入到厕所就把门关起来
            // 校验数据
            this.check_mobile();
            this.check_image_code();
            if (this.error_mobile == true || this.error_image_code == true) {
                this.send_flag = false;
                return;
            }
            // url='/sms_codes/?13236553692/?image_code=c3dt&uuid=de3422342352'
            let url = '/sms_codes/' + this.mobile + '/?image_code=' + this.image_code + '&uuid=' + this.uuid;
            axios.get(url, {responseType: 'JSON'})
                .then((response) => {
                    if (response.data.code == '0') {
                        let num = 60;
                        let t = setInterval(() => {
                            if (num == 1) {
                                clearInterval(t);
                                this.sms_code_tip = '获取短信验证码';
                                this.generate_image_code();
                                this.send_flag = false;
                            } else {
                                num -= 1;
                                this.sms_code_tip = num + '秒';
                            }
                        }, 1000)
                    } else {
                        if (response.data.code == '4001') {//图形验证码错误
                            this.error_image_code_message = response.data.errmsg;
                            this.error_image_code = true;
                            // }else if (response.data.code == '4003'){//缺少参数4003
                            //     error_sms_code_message=
                        } else {
                            //4002 频繁发送短信验证码
                            this.error_sms_code = true;
                            this.error_sms_code_message = response.data.errmsg;
                        }
                        this.send_flag = false;
                    }
                })
                .catch((error) => {
                    console.log(error.response);
                    this.send_flag = false;
                })
        },
        //校验手机验证码
        check_sms_code(){
            if (this.sms_code.length != 6) {
                this.error_sms_code = true;
                this.error_sms_code_message = '请填写6位短信验证码'
            } else {
                this.error_sms_code = false;
            }
        },

        // 校验用户名
        check_username(){
            let re = /^[a-zA-Z0-9_-]{5,20}$/; // 用户名要求
            if (re.test(this.username)) {
                this.error_name = false;
            } else {
                this.error_name_message = '请输入5-20个字符的用户名';
                this.error_name = true;
            }
            // 判断用户名是否注册
            if (this.error_name == false) {
                // let url=/usernames/itcast/count
                let url = '/usernames/' + this.username + '/count/';
                axios.get(url, {responseType: 'JSON'})
                    .then((response) => {
                        if (response.data.count == 1) {
                            this.error_name = true;
                            this.error_name_message = '用户名已存在'
                        } else {
                            this.error_name = false
                        }
                    })
                    .catch((error) => {
                        console.log(error.response)
                    })
            }
        },
        // 校验密码
        check_password(){
            let re = /^[0-9A-Za-z]{8,20}$/;
            if (re.test(this.password)) {
                this.error_password = false;
            } else {
                this.error_password = true;
            }
        },
        // 校验确认密码
        check_password2(){
            if (this.password != this.password2) {
                this.error_password2 = true;
            } else {
                this.error_password2 = false;
            }
        },
        // 校验手机号
        check_mobile(){
            let re = /^1[3-9]\d{9}$/;
            if (re.test(this.mobile)) {
                this.error_mobile = false;
            } else {
                this.error_mobile_message = '您输入的手机号格式不正确';
                this.error_mobile = true;
            }
            if (this.error_mobile == false) {
                let url = '/mobiles/' + this.mobile + '/count/';
                axios.get(url, {responseType: 'JSON'})
                    .then((response) => {
                        if (response.data.count == 1) {
                            this.error_mobile = true;
                            this.error_mobile_message = '手机号码已存在';
                        } else {
                            this.error_mobile = false;
                        }

                    })
                    .catch((error) => {
                        console.log(error.response);
                    })
            }
        },
        //验证图片验证码
        check_image_code(){
            if (this.image_code.length != 4) {
                this.error_image_code = true;
                this.error_image_code_message = '请填写图片验证码'
            } else {
                this.error_image_code = false;
            }
        },
        // 校验是否勾选协议
        check_allow(){
            if (!this.allow) {
                this.error_allow = true;
            } else {
                this.error_allow = false;
            }
        },
        on_submit(){
            this.check_username();
            this.check_password();
            this.check_password2();
            this.check_mobile();
            this.check_allow();
            this.check_sms_code();

            if (this.error_name == true || this.error_password == true || this.error_password2 == true
                || this.error_mobile == true || this.error_allow == true || this.error_sms_code == true) {
                window.event.returnValue = false;//禁用表单数据提交事件
            }
        }
    }
});