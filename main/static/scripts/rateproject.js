$(function() {
    $('.chart').easyPieChart({
        //your options goes here
    });
});

$(document).ready(function(){

    var project_id = $("#project_id").val()

    $('#ratingform').submit(function(event){

        event.preventDefault()
        form = $("#ratingform")

        $.ajax({
            'url' : '/ajax/rate/'+ project_id,
            'type': 'POST',
            'data': form.serialize(),
            'dataType': 'json',
        })
        .done(function(data){
            console.table(data);
            $(".rate"+data.uid+" .t-design").text(data.design)
            $(".rate"+data.uid+" .t-usability").text(data.usability)
            $(".rate"+data.uid+" .t-content").text(data.content)
            
        }) 
        //Ajax end function
        $("#id_design").val('')
        $("#id_usability").val('')
        $("#id_content").val('')
    })//submit end function

}) //document ready function end