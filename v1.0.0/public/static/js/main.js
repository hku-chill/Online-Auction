

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
                swal("Success", response?.message, "success").then(e => {
                    document.location.href = "../";
                });
                $(".tc_valide_button").prop("disabled", false).toggleClass("animate-pulse");
            }
            else{
                swal("Error", "Your account has not been verified, please check your informations...", "error");
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