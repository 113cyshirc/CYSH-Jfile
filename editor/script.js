let tests_count = 0;
let letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"," ","1","2","3","4","5","6","7","8","9","0"]
let msging = false;

$(document).ready(function () {
    $("#question_tab").click(function () { 
        $("#question").show();
        $(this).css("background-color","#5f5f5f");
        $("#tests_tab").css("background-color","#1f1f1f");
        $("#tests").hide();
    });
    $("#tests_tab").click(function () { 
        $("#tests").show();
        $(this).css("background-color","#5f5f5f");
        $("#question_tab").css("background-color","#1f1f1f");
        $("#question").hide();
    });
    $("#new").click(function () {
        new_file();
    });
    $("#folder").click(function () {
        get_folder($("#path").val());
    });
    $("#pack").click(function () {
        pack($("#path").val());
    })
    $("#save").click(function () {
        save();
    });
    add_keysound();
    
});

function gen_unicode() {
    if ([...$("#title").val()].every(n => letters.includes(n))) {
        $("#titleUnicode").val($("#title").val());
    }
    if ([...$("#author").val()].every(n => letters.includes(n))) {
        $("#authorUnicode").val($("#author").val());
    }
}

function add_keysound() {
    addEventListener("keydown",(e) => {
        if (e.code.startsWith("Key")||e.code.startsWith("Digit")||e.code.startsWith("Space")) {
                if (letters.includes(e.code.slice(-1).toLowerCase())) {
                document.getElementById("key1").play();
            }
        }else if (e.code == "Backspace"){
            document.getElementById("key2").play()
        }
    });
    addEventListener("select",(e) => {
        document.getElementById("select").play();
    });
    $(".click_s").click(function(){
        document.getElementById("click_s").play();
    })
}

function new_file() {
    setInterval(gen_unicode,100);
    $("#question").html(` <table>
                <tr>
                    <td><p>標題</p></td>
                    <td><input type="text" id="title"></td>
                </tr>
                <tr>
                    <td><p>英文或羅馬拼音標題</p></td>
                    <td><input type="text" id="titleUnicode"></td>
                </tr>
                <tr>
                    <td><p>作者名</p></td>
                    <td><input type="text" id="author"></td>
                </tr>
                <tr>
                    <td><p>作者名(英文或羅馬拼音)</p></td>
                    <td><input type="text" id="authorUnicode"></td>
                </tr>
                <tr>
                    <td><p>你的名字</p></td>
                    <td><input type="text" id="Creator"></td>
                </tr>
                <tr>
                    <td><p>來源</p></td>
                    <td><input type="text" id="Source"></td>
                </tr>
                <tr>
                    <td><p>標籤</p></td>
                    <td><input type="text" id="Tags"></td>
                </tr>
                <tr>
                    <td><p>提示</p></td>
                    <td><input type="text" id="Hint"></td>
                </tr>
                <tr>
                    <td><p>執行時間限制(s)</p></td>
                    <td><input type="number" id="Time" min="1" step="0.5" value="1"></td>
                </tr>
                <tr>
                    <td><p>執行記憶體限制(Mb)</p></td>
                    <td><input type="number" id="Memory" min="100" step="100" value="100"></td>
                </tr>
                <tr>
                    <td><p>範例測資數</p></td>
                    <td><input type="number" id="SampleTests" min="1" step="1" value="1"></td>
                </tr>
                <tr>
                    <td><p>參數名字(一個一行)</p></td>
                    <td><textarea name="" id="args" rows="5"></textarea></td>
                </tr>
                <tr>
                    <td><p>題目</p></td>
                    <td><textarea name="" id="Question" rows="5"></textarea></td>
                </tr>
                <tr>
                    <td><p>輸入說明</p></td>
                    <td><textarea name="" id="in" rows="5"></textarea></td>
                </tr>
                <tr>
                    <td><p>輸出說明</p></td>
                    <td><textarea name="" id="out" rows="5"></textarea></td>
                </tr>
            </table>`);
    $("#tests").html(`<div id="all_tests"></div><div class="new_test click_s">新增測資</div>`);
    $(".new_test").click(function () {
        let amount = prompt("請問要新增多少測資");
        if (parseInt(amount) != NaN) {
            for (let i=0;i<parseInt(amount);i++) {
                tests_count++;
                $("#all_tests").append(`
                    <div class="test_box">
                        <table style="width: 95%;">
                            <caption>測資${tests_count}</caption>
                            <tr>
                                <td><p>輸入</p></td>
                                <td><textarea name="in" id="in${tests_count}" rows="5" style="width: 100%;"></textarea></td>
                            </tr>
                            <tr>
                                <td><p>輸出</p></td>
                                <td><textarea name="in" id="out${tests_count}" rows="5" style="width: 100%;"></textarea></td>
                            </tr>
                        </table>
                    </div>`);
            }
        }else {
            alert("欸!給我輸入數字");
        }
        
    });
}

function save() {
    result = {};
    result["path"] = $("#path").val();

    result["question"] = {
        '_format': 3,
        '_comment0': ' General',
        'Difficulty': '',
        'CompatibilityMode': 'False',
        'SampleTests': $("#SampleTests").val(),
        'Tests': '',
        'LastUpdate': '0',
        '_comment1': ' Metadata',
        'Title': $("#title").val(),
        'TitleUnicode': $("#titleUnicode").val(),
        'author': $("#author").val(),
        'authorUnicode': $("#authorUnicode").val(),
        'Creator': $("#Creator").val(),
        'Version': '0',
        'Source': $("#Source").val(),
        'Tags': $("#Tags").val(),
        'Hint': $("#Hint").val(),
        'QuestionID': '',
        'QuestionSetID': '',
        '_comment2': ' limit',
        'Time': $("#Time").val(),
        'Memory': $("#Memory").val(),
        'args': [], // process later
        'question': ($("#Question").val().includes("\n")?$("#Question").val():$("#Question").val()+"\n"),
        'in': ($("#in").val().includes("\n")?$("#in").val():$("#in").val()+"\n"),
        'out': ($("#out").val().includes("\n")?$("#out").val():$("#out").val()+"\n")
    };
    $("#args").val().split("\n").forEach(element => {
        if (element != "") {
            result["question"]['args'].push(element);
        }
    });
    result["question"]['Tests'] = $(".test_box").length.toString();

    result["tests"] = [];
    for (let i=0;i<$(".test_box").length;i++) {
        let _in = []
        let _out = []
        $(`#in${i+1}`).val().split("\n").forEach(element => { // read all in value
            if (element != "") {
                _in.push(element);
            }
        });
        $(`#out${i+1}`).val().split("\n").forEach(element => { //read all in value
            if (element != "") {
                _out.push(element);
            }
        });
        result["tests"].push([_in,_out,false]);
    }

    if (verify(result)) {
        $.post(`./save?jsn=${JSON.stringify(result)}`,function(success) {
        if (success) {
            message(true,"儲存成功");
        }else {
            message(false,"儲存失敗");
        }
    }); 
    }
    
}

function pack(path) {
    $.post(`/pack?path=${path}`,function(r) {
        if (r) {
            message(true,"成功打包");
        }else {
            message(false,"打包失敗");
        }
    });
}

function get_folder(path) {
    new_file();
    $.post(`/getFolder?path=${path}`,function(r) {
        if (r) {
            result = JSON.parse(r);
            
            // question
            $("#title").val(result["question"]["Title"]);
            $("#titleUnicode").val(result["question"]["TitleUnicode"]);
            $("#author").val(result["question"]["author"]);
            $("#authorUnicode").val(result["question"]["authorUnicode"]);
            $("#Creator").val(result["question"]["Creator"]);
            $("#Source").val(result["question"]["Source"]);
            $("#Tags").val(result["question"]["Tags"]);
            $("#Hint").val(result["question"]["Hint"]);
            $("#Time").val(parseInt(result["question"]["Time"]));
            $("#Memory").val(parseInt(result["question"]["Memory"]));
            $("#SampleTests").val(parseInt(result["question"]["SampleTests"]));
            // args will be build later
            $("#Question").val(result["question"]["question"].slice(0,-1));
            $("#in").val(result["question"]["in"].slice(0,-1));
            $("#out").val(result["question"]["out"].slice(0,-2));
            // tags
            let arg = ""
            result["question"]["args"].forEach(e => {
                arg += `${e}\n`
            });
            $("#args").val(arg.slice(0,-1));

            // tests
            tests_count = 0;
            appendTest(result["tests"]);
        }else {
            message(false,"載入失敗");
        }
        
    })
}

function verify(dict) {
    // 輸入量檢測
    if (dict["path"] == "") {
        alert("儲存路徑不可以為空白");
        return false
    }else if (!(parseInt(dict["question"]["Tests"]) > 0)) {
        alert("請新增測資");
        return false
    }else if (dict["question"]["SampleTests"] == "" || parseInt(dict["question"]["SampleTests"])<1 || parseInt(dict["question"]["SampleTests"])>parseInt(dict["question"]["Tests"])) {
        alert("範例測資數不正確");
        return false
    }else if (dict["question"]["question"] == ""||dict["question"]["question"] == "\n") {
        alert("請輸入問題");
        return false
    }else if (dict["question"]["in"] == ""||dict["question"]["in"] == "\n") {
        alert("請輸入輸入描述");
        return false
    }else if (dict["question"]["out"] == ""||dict["question"]["out"] == "\n") {
        alert("請輸入輸出描述");
        return false
    }
    // 內容檢測
    else {
        let titleUni = true;
        let authorUni = true;
        dict["question"]["TitleUnicode"].split("").forEach(element => {
            if (!letters.includes(element.toLowerCase())) {
                titleUni = false;
            }
        });
        dict["question"]["authorUnicode"].split("").forEach(element => {
            if (!letters.includes(element.toLowerCase())) {
                authorUni = false;
            }
        });
        if (!titleUni) {
            alert("請確定英文或羅馬拼音標題");
            return false;
        }else if (!authorUni) {
            alert("請確定英文或羅馬拼音作者名");
            return false;
        }
        return true;
    }
}

function appendTest(l){
    console.log(l)
    l.forEach(e => {
        if (!e[2]) {
            let _in = "";
            e[0].forEach(e => {
                _in += `${e}\n`;
            });
            _in = _in.slice(0,-1);
            let _out = "";
            e[1].forEach(e => {
                _out += `${e}\n`;
            });
            _out = _out.slice(0,-1);
            tests_count++;
            $("#all_tests").append(`
                <div class="test_box">
                    <table style="width: 95%;">
                        <caption>測資${tests_count}</caption>
                        <tr>
                            <td><p>輸入</p></td>
                            <td><textarea name="in" id="in${tests_count}" rows="5" style="width: 100%;">${_in}</textarea></td>
                        </tr>
                        <tr>
                            <td><p>輸出</p></td>
                            <td><textarea name="in" id="out${tests_count}" rows="5" style="width: 100%;">${_out}</textarea></td>
                        </tr>
                    </table>
                </div>`);
        }
    });
}

function message(success,msg) {
    if (!msging) {
        msging = true;
        $("#message").text(msg);
        if (success) {
            $(".message").css("background-color","green");
        }else {
            $(".message").css("background-color","red");
        }
        $(".message").fadeIn(1000).fadeOut(2000,function() {msging = false;})
    }
    
}