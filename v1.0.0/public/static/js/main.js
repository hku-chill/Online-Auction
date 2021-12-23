

// TC dogrulama javascript fonksiyonu
$(".tc_verify_form").submit(function (e) { 
    e.preventDefault();

    $(".tc_valide_button").prop("disabled", true).toggleClass("animate-pulse");
    $.ajax({
        type: "POST",
        url: $(this).attr('action'),
        data: $(this).serialize(),
        success: function (response) {
            if (response?.success === true){
                Swal.fire("Success", response?.message, "success").then(e => {
                    document.location.href = "../";
                });
                $(".tc_valide_button").prop("disabled", false).toggleClass("animate-pulse");
            }
            else{
                Swal.fire("Error", "Your account has not been verified, please check your informations...", "error");
                $(".tc_valide_button").prop("disabled", false).toggleClass("animate-pulse");
            }
        },
        Error: function (response) {
            alert("something went wrong please contact to admin: "+response).then(e => {
                document.location.href = "../";
            })
            $(".tc_valide_button").prop("disabled", false).toggleClass("animate-pulse");
        }
    });

    return false;

});

//add bid javascript
$(document).on("click",".add_bid_button",function (e) { 
    e.preventDefault();
    request_uri = $(this).attr("requ-uri")

    $.ajax({
        type: "GET",
        url: request_uri,
        data: {
            "request_form": true
        },
        success: function (response, textStatus, xhr) {
            if (typeof response === "object" && response.success === false){
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: response.message,
                    footer: response.footer ? `<a href="${response.footer.url }">${response.footer.text}</a>` : ''
                })
                return false;
            }
            if(xhr.status == 200){

                Swal.fire({
                    title: 'Add bid to auction',
                    html: response,
                    confirmButtonText: 'Send Bid',
                    focusConfirm: false,
                    preConfirm: () => {
                      const csrf = Swal.getPopup().querySelector('[name="csrfmiddlewaretoken"]').value
                      const bid = Swal.getPopup().querySelector('[name="bid_amount"]').value
                      if (!csrf || !bid) {
                        Swal.showValidationMessage(`Please fill all fields!`)
                      }
                      return { csrf: csrf, bid: bid }
                    }
                  }).then((result) => {
                    $.ajax({
                        type: "post",
                        url: request_uri,
                        data: {bid_amount: result.value.bid, csrfmiddlewaretoken: result.value.csrf, addBid_form: true},
                        success: function (response) {
                            Swal.fire({
                                icon: response.success ? 'success' : 'error',
                                title: 'Humbl Bid',
                                text: response.message,
                                footer: response.footer ? `<a href="${response.footer.url }">${response.footer.text}</a>` : ''
                            }).then(e => location.reload())

                            
                        }
                    });
                  })

            }
        },
        error: function (response) {
            alert("something went wrong please contact to admin: "+response).then(e => {
                document.location.href = "../";
            })
        }
    });
});


$(document).on({
    mouseenter: function (e) {
        //over
        $(".auction-rate .fas").removeClass("fas").addClass("far");
        for (const i of $(".auction-rate i")) {
            

            $(i).removeClass("far").addClass("fas");
            if (i === this){
                return
            }
        }
    },
    mouseleave: function (e) {
        for (const i of $(".auction-rate i")) {
            $(i).hasClass("added") ? $(i).removeClass("far").addClass("fas") : $(i).removeClass("fas").addClass("far");
        }
    }
},".auction-profile .auction-rate i");

$(document).on("click",".auction-profile .auction-rate i", function (e) {
    e.preventDefault()
    let it = 1;
    const slug = $("section.auction-profile").attr("auction-slug")
    if(!slug) return

    for (const i of $(".auction-rate i")) {
            
        if (i === this){
            break
        }

        it++
    }
    
    $.ajax({
        type: "GET",
        url: "/auction/rate-auction",
        data: {
            "rate": it,
            "auction-slug": slug
        },
        success: function (response) {
            if (response?.success === true){
                Swal.fire({
                    icon: 'success',
                    title: 'Success',
                    text: response.message
                }).then(e => {
                    location.reload()
                })
                
            }
            else{
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: response.message,
                    footer: response.footer ? `<a href="${response.footer.url }">${response.footer.text}</a>` : ''
                })
                return false;
            }
        }
    })
});

$(document).ready(function () {
    
    var endDate = $(".bid-data-alt-info.bid-data-enddate");
    if (!endDate.length > 1) {
        return false;
    }

    

    function e(isrest= false, isrest_in = null){
        const endDateTime = new Date(isrest_in || endDate.attr("enddate"))
        const now = new Date();
        const distance = endDateTime - now;
        var timer;

        if(isrest){
            if(distance < 0 ) return "Ended"
            const days = Math.floor(distance / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));

            return `${days >= 10 ? days : "0"+days }:${minutes >= 10 ? minutes : "0"+minutes}`
        }

        if (distance < 0) {
            endDate.html("<span class='text-danger'>Bid is ended</span>");
            clearInterval(timer);
        } else {
            const days = Math.floor(distance / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);
            
            $(endDate).html(`${days}:${minutes}:${seconds}`);
        }
    }

    var static_calc = $(".calculate_rest")
    for (const i of static_calc) {
        $(i).html(e(true, $(i).attr("enddate")))
    }

    timer = setInterval(e, 1000);

});














function IsJsonString(str) {
    try {
        JSON.parse(str);
    } catch (e) {
        return false;
    }
    return true;
}








//adding new keyword
$(".add_keyword_button").on("click touch", function (e) {
    e.preventDefault()
    const keyword = $(this).parent().find("#keyword_input").val()
    
    if(keyword && keyword != null && keyword != ""){
        $(".keyword-list .item-list").append( $('<div/>',{
            class: "keyword-item",
            text: keyword
        }));
        $(this).parent().find("#keyword_input").val("")
    }else{
        $(this).parent().find("#keyword_input").focus()
    }
});

//removing keyword
$(document).on("click touch",".keyword-list .keyword-item", function (e) {
    e.preventDefault()
    $(this).remove()
})



//category selection
$(".category-list .category-item").on("click touch", function (e) {
    e.preventDefault()
    $(".category-list .category-item").removeClass("selected")
    const category_input = $("#id_category")
    let ss = $(this).toggleClass("selected").attr("category-slug");
    $(category_input).val(ss);
})


function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('img.target_img').attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }
}


//auction createin on image selected

$("#id_item_image").change(function (e) { 
    e.preventDefault();
    readURL(this)
});





//report section

$(document).on("click","div.report_container", function (e) {
    var block = $(".report_block");
    if (!block.is(e.target) && block.has(e.target).length === 0 || $(".report_close_button").is(e.target)) 
    {
        $(".report_container").toggleClass("hidden")
    }



    //check if input clicks
    if($(".reason_item").is(e.target)){
        $(e.target).addClass("selected").siblings().removeClass("selected")
        $(".report_container #hidden_input_reason").val($(e.target).html())
    }
});


$(document).on("click","a.report_it_button", function (e) {
    e.preventDefault()
    //$(this).attr("report-type")
    $(".report_container").toggleClass("hidden")

    //set values for inputs
    $(".report_container #hidden_input_type").val($(this).attr("report-type"))
    $(".report_container #hidden_input_id").val($(this).attr("report-id"))
});


$(document).on("submit","form.report_form", function (e) {
    e.preventDefault()
    $.ajax({
        type: "POST",
        url: $(this).attr("action"),
        data: $(this).serialize(),
        success: function (response) {
            if (response?.success === true){
                Swal.fire({
                    icon: 'success',
                    title: 'Success',
                    text: response.message
                }).then(e => {
                    location.reload()
                })
                
            }
            else{
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: response.message,
                    footer: response.footer ? `<a href="${response.footer.url }">${response.footer.text}</a>` : ''
                })
                return false;
            }
        }
    });
});