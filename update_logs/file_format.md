# 檔案格式更新紀錄

## v1
### 類型
- **format version**
- **classifier**
- **key,value**
- **list**
- **str**

### 格式
#### cjf
    CYSHJ file format v1            <--format version

    [general]                       <--classifier
    Difficulty:1.0                  <--key:value
    CompatibilityMode:False          
    SampleTests:3
    Tests:9

    [Metadata]                      <--classifier
    Title:哈囉
    TitleUnicode:哈囉
    author:布萊恩·克尼漢
    authorUnicode:Brian Kernighan
    Creator:Know Scratcher
    Version:0
    Source:Brian Kernighan
    Tags:基本輸出輸入
    QuestionID:001
    QuestionSetID:a001

    [args]
    name                            <--list

    [question]
    輸入名字，輸出「hello, 名字」。   <--str

#### cjt
    [in]
    40

    [out]
    NO

    [in]
    100

    [out]
    YES

    [in]
    168

    [out]
    YES

## v2
### 更新原因
- 讀取類型不確定
- 無法註解
- 寫死的讀取

### 類型
- format version
- classifier
- **content type**
- key,value
- list
- str
- **comment**

### 格式
    CYSHJ file format v2            <--format version

    [general]                       <--classifier
    Difficulty:1.0                  <--key:value
    CompatibilityMode:False          
    SampleTests:3
    Tests:9

    [Metadata]                      <--classifier
    Title:哈囉
    TitleUnicode:哈囉
    author:布萊恩·克尼漢
    authorUnicode:Brian Kernighan
    Creator:Know Scratcher
    Version:0
    Source:Brian Kernighan
    Tags:基本輸出輸入
    QuestionID:001
    QuestionSetID:a001

    [l:args]                        <--content type:classifier
    name                            <--list

    [s:question]                    <--content type:classifier
    輸入名字，輸出「hello, 名字」。   <--str
    //comment                       <--comment

### 註解
- cjt無更新