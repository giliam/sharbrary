var rating_informations = ["{{opinion_notation_values.0.1|safe}}","{{opinion_notation_values.1.1|safe}}","{{opinion_notation_values.2.1|safe}}","{{opinion_notation_values.3.1|safe}}","{{opinion_notation_values.4.1|safe}}","{{opinion_notation_values.5.1|safe}}"];
var current_value = [];
$( document ).ready(function() {
    $('.rates').click(function(){
    var data, catid, book_id;
    data = $(this).attr("id").replace('rate_','').split("_");
    catid = data[0];
    book_id = data[1];
    $.get("{% url "book_rate" 0 0 %}".replace("/0/0/", "/" + book_id + "/0/").replace('/0/',"/" + catid + "/"), function(data){});
    current_value[book_id] = catid;
    $('#rating_information_' + book_id).text(rating_informations[current_value[book_id]]);
});

$('.rating_stars').hover(function(){
    var data, catid, book_id;
    data = $(this).attr("id").replace('rate_star_','').split("_");
    catid = data[0];
    book_id = data[1];
    $('#rating_information_' + book_id).text(rating_informations[catid]);
    for (var i = 1; i <= 5; i++) {
        if(i<=catid){
            $('#rate_star_' + i + "_" + book_id).attr("src", "{% static 'img/star_full.png' %}");
        }else{
            $('#rate_star_' + i + "_" + book_id).attr("src","{% static 'img/star_empty.png' %}");
        }
    }
});

$('.rates').hover(function(){},function(){
    var data, catid, book_id;
    data = $(this).attr("id").replace('rate_','').split("_");
    catid = data[0];
    book_id = data[1];
    $('#rating_information_' + book_id).text(rating_informations[current_value[book_id]]);
    for (var i = 1; i <= 5; i++) {
        if(i<=current_value[book_id]){
            $('#rate_star_' + i + "_" + book_id).attr("src", "{% static 'img/star_full.png' %}");
        }else{
            $('#rate_star_' + i + "_" + book_id).attr("src","{% static 'img/star_empty.png' %}");
        }
    }
});
});