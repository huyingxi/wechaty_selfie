/**
 * Created by wangqi on 2017/5/17.
 */
/*用户发送'selfie',回复"请发一张你的头像"。
* 用户回复消息为图片格式,则获取评分。否则,回复"发送的不是图片格式,请重新发送selfie"
*
* 用户发送'selfie',则开启bot.on('message',selfie)监听,并将用户存入列表中
* 若列表为空,则移除监听。*/

import {Wechaty,Room,Config,Message} from 'wechaty';
import { createWriteStream, writeFileSync }  from 'fs'

const bot=Wechaty.instance();
var needle = require('needle');
var selfieList=[];
bot
    .on('scan', (url, code)=>{
        let loginUrl = url.replace('qrcode', 'l')
        require('qrcode-terminal').generate(loginUrl)
        console.log(url)
    })

    .on('login', user => console.log(`User ${user} logined`))

    .on('message',  async function(m){
        const contact=m.from();     console.log("人");
        const content=m.content();
        const room=m.room();
        if(room){
            console.log(`Room:${room.topic()}、${contact}发来${content}`)
        }else{
            console.log(`${contact}:${content}`)
        }
        if(m.self()) return;  console.log('speak')
        if(/^selfie$/i.test(content)){       //忽略大小写
            m.say('请发一张你的头像');
            if(selfieList.length==0){       //如果列表为空,说明没有selfie监听。
                selfieList.push(contact);

                bot.on('message',async function selfie(n) {  console.log('selfie监听')
                    const contact1=n.from();
                    const content1=n.content();
                    if(/^selfie$/i.test(content1)||n.self()) return;   //如果是selfie命令,就不继续。防止重复发送'selfie'出错。
                    console.log('speak2');
                    selfieList.forEach((person,index)=>{   //如果在列表中且是同一个人。
                        if(person==contact1){

                            if(n.type()==3){  //发送的是图片格式
                                n.say(`${contact1},我们正在飞速分析您的照片,请耐心等待。`);
                                saveMediaFile(n);

                            }else{
                                n.say('发送的不是图片格式,请重新发送selfie.');
                            }

                            selfieList.splice(index,1)//移除这个人
                            return  //每个人只可能出现一次,所以出现一次后,就终止。
                        }
                    })
                    if(!selfieList.length) bot.removeListener('message',selfie);  //如果列表为空,则移除监听。
                })
            }

            else if(!selfieList.includes(contact)) selfieList.push(contact); //列表中如果已有此人,就不添加。

        }

    })

    .init()

function saveMediaFile(message) {
    const filename = message.filename()
    console.log('IMAGE local filename: ' + filename)

    const fileStream = createWriteStream('../image/'+filename)

    console.log('start to readyStream()')
    message.readyStream()
        .then(stream => {   //下载图片到本地
            stream.pipe(fileStream)
                .on('close', () => {
                    console.log('finish readyStream()');
                    var data = [{
                        file: '../image/'+filename,
                        content_type: 'image/png'
                    }];
                    needle
                        .post('111.207.243.71:8000/Imagetest', data, { multipart: true },function (err,res) {
                            message.say(`你的头像得分是${res.body.data}分!您这是帅炸了啊!`);
                                   })
        })
         .catch(e => console.log('stream error:' + e))
})}





