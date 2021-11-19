$(document).ready(function(){

    $('form').on('submit', function(event){

        var r = {};
        $(".reacts").each(function(){
           r[$(this).attr('id')] = $(this).val();
        });

        var p = {};
        $(".prods").each(function(){
           p[$(this).attr('id')] = $(this).val();
        });

        $.ajax({
            data: {
                // reacts: $("#react0").val(),
                reacts: JSON.stringify(r),
                // prods: $("#prod0").val()
                prods: JSON.stringify(p)
            },
            type: "POST",
            url : "/process"
        })
        .done(function(data){
            // $('#holder').append(data["reaction_info"]);

            $.each(data["reaction_info"], function(index, element){
                if (index == 0){
                    var x = $('<span>&times;</span>').attr("class", "w3-button w3-display-right")
                    .click(function() {this.parentElement.remove()});
                    var t = $('<li></li>').text(element).attr("class", "w3-display-container").append(x);
                    $('#MM').before(t);
                } else {
                $.each(element, function(index, elt){
                    var l = $('<span>&times;</span>').attr("class", "w3-button w3-display-right")
                    .click(function() {this.parentElement.remove()});
                    // .click(function() {this.parentElement.style.display='none'});
                    var t = $('<li></li>').text(elt).attr("class", "w3-display-container").append(l);
                    $('#holder').append(t);
                })
                }
            });

            var seen = {};
            $('li').each(function() {
                var txt = $(this).text();
                if (seen[txt]){
                    $(this).remove();
                }else{
                    seen[txt] = true
                };
            });

            $("#holder").show();
        });

        event.preventDefault();

    });


    function newReact(counter){
        var l = $('<span>&times;</span>').attr("class", "w3-button w3-display-right")
                    .click(function() {this.parentElement.remove()});
        var t = $("<input>").attr("placeholder", "reactivo").attr("id", "react" + counter)
        .addClass("reacts w3-input w3-border").attr("type", "text").attr("list", "molecules_list");
        // $("#reactivos").append(t);
        $("#reactivos").append($("<div></div>").attr("class", "w3-half w3-display-container").append(t).append(l));
    };

    function newProd(counter){
        var l = $('<span>&times;</span>').attr("class", "w3-button w3-display-right")
                    .click(function() {this.parentElement.remove()});
        var t = $("<input>").attr("placeholder", "producto").attr("id", "prod" + counter)
        .addClass("prods w3-input w3-border").attr("type", "text").attr("list", "molecules_list");
        // $("#productos").append(t);
        $("#productos").append($("<div></div>").attr("class", "w3-half w3-display-container").append(t).append(l))
    };

    const newReact2 = (function () {
    let counter = 0;
    return function () {counter += 1; return newReact(counter)}
    })();

    const newProd2 = (function () {
    let counter = 0;
    return function () {counter += 1; return newProd(counter)}
    })();

    $("#nuevo_reactivo").click(function(){return newReact2()})
    $("#nuevo_producto").click(function(){return newProd2()})


    $('#limpiar').click(function() {
        $("li:has(span)").remove();
    });


});




