write_question = function(id,text){
    var question = '<span id="'+id+'" class="question_button">'+text+'</span>';
    $('#questions_container').append(question);
};

questions_box = function(topicId){
    $.ajax({
        url:'/questionslist/',
        type:'POST',
        data:{'topicId':topicId},
        success:function(data){
            $('#questions_container').html('');
            for(var d in data){
                write_question(data[d]['id'],data[d]['text']);
            }
            $('#questions_container').hide(0);
            $('#questions_container').fadeIn('slow');
        }
    });
};

write_answer_and_dialog = function(sender,data){
    var content = '<span id="answer+'+$(sender).attr('id')+'" class="answer"\
    style="display:none;">'+data+'</span>'
    var DIALOG = '\
    <div id="globe_faq_form" style="display:none;">\
        <div id="form_title">&iquest;A&uacute;n con dudas?, escr&iacute;benos.</div>\
        <table width="278" border="0">\
            <tr>\
                <td width="144">\
                    <input type="text" id="name" value="Nombre"/>\
                </td>\
                <td colspan="2" rowspan="2">\
                    <textarea id="comment" cols="5" rows="5">Comentario</textarea>\
                </td>\
            </tr>\
            <tr>\
                <td>\
                    <input type="text" id="email" value="Correo@servidor.com"/>\
                </td>\
            </tr>\
            <tr>\
                <td valign="middle" id="error_area">&nbsp;</td>\
                <td width="38" align="right" style="color:#edeeee; opacity:0;">a</td>\
                <td align="right" width="150">\
                    <input type="button" id="send_button" value="Enviar" />\
                </td>\
            </tr>\
        </table>\
    </div>'
    $(content+DIALOG).insertAfter(sender);
};

answer = function(sender){
    $.ajax({
        url:'/answer/',
        type:'POST',
        data:{'questionId':$(sender).attr('id')},
        success:function(data){
            answer_id = write_answer_and_dialog(sender,data);
            $('.answer').slideDown('slow');
            $('#globe_faq_form').slideDown('slow');
        }
    });
};

remove_answer_contact_area = function(){
    $('.answer').slideUp('slow',function(){
        $('.answer').remove();
    });
    $('#globe_faq_form').slideUp('slow',function(){
        $('#globe_faq_form').remove();
    });
};

question_contact = function(question){
    $.ajax({
        url:'/questioncontact/',
        type:'POST',
        data:{
            'question':question,
            'name':$('#name').val(),
            'email':$('#email').val(),
            'comment':$('#comment').val()
        },
        success:function(){
            $('#notice').slideDown('slow').delay(2000).slideUp('slow');
            remove_answer_contact_area();
        }
    });
};
