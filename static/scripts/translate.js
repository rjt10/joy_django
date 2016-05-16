var TranslationBox = React.createClass({
    getTranslationFromServer: function () {
        $.ajax({
            url: '/joy/translate',
            dataType: 'json',
            cache: false,
            success: function(data) {
                console.log('resp data: ', data);
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(status, err.toString());
            }.bind(this)
        });
    },

    handleTranslationSubmit: function () {
        $.ajax({
            url: '/joy/translate',
            dataType: 'json',
            cache: false,
            success: function(data) {
                console.log('resp data: ', data);
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(status, err.toString());
            }.bind(this)
        });
    },

    render: function () {
        return (
             <div className='translationBox'>
                <h1>Play with translation!</h1>
                <TranslationForm onTranslationSubmit={this.handleTranslationSubmit} />
                <TranslationList />
            </div>
        );
    }
});

var TranslationList = React.createClass({
    render: function () {
        return (
            <div className='translationList'>
                <h3>this is a translation list</h3>
            </div>
        );
    }
});

var TranslationForm = React.createClass({
    getInitialState: function () {
        return {
            src: 'en',
            tgt: 'de',
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
        this.setState({tgt: e.target.val});
    },

    handleSubmit: function (e) {
        e.preventDefault();
        let txt = this.state.txt.trim();
        let src = this.state.src.trim();
        let tgt = this.state.tgt.trim();

        if (!txt) {
            return;
        }
        let q = {src: src, tgt: tgt, txt: txt}
        console.log('q:' + JSON.stringify(q));
        $.ajax({
            method: 'GET',
            url: '/joy/translate',
            data: q,
            cache: false,
            success: function(data) {
                console.log(JSON.stringify(data));
            }.bind(this),
            error: function(xhr, status, err) {
                console.log(status, err);
            }.bind(this)
        });
    },

    render: function () {
        return (
            <form className='translationForm' onSubmit={this.handleSubmit}>
                <h2> this is a translation form </h2>
                <input type="text" placeholder="Say something..." value={this.state.txt} onChange={this.handleTxtChange} />
                <input type="submit" value="Translate" />
            </form>
        );
    }
});

ReactDOM.render(
    <TranslationForm />,
    document.getElementById('content')
);