

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

//add bid javascript



$(document).ready(function () {
    
    var endDate = $(".bid-data-alt-info.bid-data-enddate");
    if (!endDate.length > 1) {
        return false;
    }

    function e(){
        const endDateTime = new Date(endDate.attr("enddate"))
        const now = new Date();
        const distance = endDateTime - now;
        var timer;

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