Vue的大胡子语法 和Django/flask的模板语法冲突了
delimiters:["[[","]]"]
- - href="#"   当定义了a 的属性href = ‘#’， 点击a标签会刷新页面并且会回到页面头部
- href = ‘；’   当定义了a 的属性href = ‘；’，点击a标签就会刷新页面
- href = ‘JavaScript：；’ 当定义了a 的属性href = ‘JavaScript：；’，意味着点击之后，用JavaScript代码来处理，但是JavaScript：代码是为空的，所以什么都不处理
- 如果使用a标签，那么你必须有href属性

this 指的是当前的Vue对象，this.属性来获取值

splice（index ， n）  从下标为index 的地地方开始删除掉n个值splice（index， 0 ， item）在下标为index 的地方进行替换成itemlist.push(元素)  js中的添加方法，是往列表中添加数据

v-bind: 简写 **:**

v-on: 简写 **@**

javascript对象的写法：

ES5写法：

```html
var person = { 
    name:'itcast',
    age:13,
    say:function(){
        alert('hello')
    }
}

person.say()
```

ES6写法：

```html
//定义变量
var name='itcast';
var age=13;
//创建对象
var person = {
    name,
    age,
    say:function(){
        alert('hello');
    }
};
//调用
person.say()
```

![1](C:\Users\FY\Desktop\截图\Vue\1.png)

![2](C:\Users\FY\Desktop\截图\Vue\2.png)

![3axios](C:\Users\FY\Desktop\截图\Vue\3axios.png)

![4 response-data-info-username](C:\Users\FY\Desktop\截图\Vue\4 response-data-info-username.png)

![7](C:\Users\FY\Desktop\截图\Vue\7.png)

![8](C:\Users\FY\Desktop\截图\Vue\8.png)

console.log(response.data.info.username);

![6response--data](C:\Users\FY\Desktop\截图\Vue\6response--data.png)