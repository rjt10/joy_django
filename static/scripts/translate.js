let translationUnitId = 1;

var TranslationBox = React.createClass({
    // 
    // Example state:
    //   {"translations":[
    //     {"translatedText":"Hola Mundo"}
    //   ]}
    // 
    getInitialState: function () {
        return { data: {}}
    },

    handleTranslationSubmit: function (translationReq) {
        console.log('translationReq:' + JSON.stringify(translationReq));
        $.ajax({
            method: 'GET',
            url: '/joy/translate',
            data: translationReq,
            cache: false,
            success: function(data) {
                console.log('resp: ' + JSON.stringify(data));
                if ('data' in data) {
                    this.setState({data: data['data']});
                }
            }.bind(this),
            error: function(xhr, status, err) {
                console.log(status, err);
                // TODO(update the UI accordingly)
            }.bind(this)            
        });
    },

    render: function () {
        return (
             <div className='translationBox'>
                <h1>Play with translation!</h1>
                <TranslationForm onTranslationSubmit={this.handleTranslationSubmit} />
                <p />
                <TranslationList data={this.state.data} />
            </div>
        );
    }
});

var TranslationList = React.createClass({
    render: function () {
        let translationResult = this.props.data;
        console.log('data for translationList: ' + JSON.stringify(translationResult));
        let translations = translationResult['translations']
        let translationUnits = null;
        if (translations != null && Array.isArray(translations)) {
            translationUnits = translations.map(function (unit) {
                translationUnitId ++;
                let translatedText = unit['translatedText']
                return (<TranslationUnit key={translationUnitId} translatedText={translatedText} />);
            });
            return (
                <div className='translationList'>
                    {translationUnits}
                </div>
            );
        }
        else {
            return null;
        }
    }
});

var TranslationUnit = React.createClass({
    render: function() {
        let translatedText = this.props.translatedText;
        return (
            <div className='translationUnit'>               
                <div className='translatedText'>
                    {translatedText}
                </div>
            </div> 
        );
    }
});

var TranslationForm = React.createClass({
    getInitialState: function () {
        return {
            src: 'en',
            tgt: 'es',
            txt: 'hello world'
        };
    },

    handleTxtChange: function(e) {
        this.setState({txt: e.target.value});
    },

    handleSrcChange: function(e) {
        this.setState({src: e.target.value});
    },

    handleTgtChange: function(e) {
        this.setState({tgt: e.target.value});
    },

    handleSubmit: function (e) {
        e.preventDefault();
        let txt = this.state.txt.trim();
        let src = this.state.src.trim();
        let tgt = this.state.tgt.trim();

        if (!txt) {
            return;
        }
        let req = {src: src, tgt: tgt, txt: txt}
        this.props.onTranslationSubmit(req);
    },

    render: function () {
        return (
            <form className='translationForm' onSubmit={this.handleSubmit}>
                <select value="en" onChange={this.handleSrcChange}>
                    <option value="es">Spanish</option>
                    <option value="en">English</option>
                    <option value="zh-CN">Chinese</option>
                </select>
                <input type="text" placeholder="Say something..." value={this.state.txt} onChange={this.handleTxtChange} />
                <select value="es" onChange={this.handleTgtChange}>
                    <option value="es">Spanish</option>
                    <option value="en">English</option>
                    <option value="zh-CN">Chinese</option>
                </select>
                <input type="submit" value="Translate" />
            </form>
        );
    }
});

ReactDOM.render(
    <TranslationBox />,
    document.getElementById('content')
);