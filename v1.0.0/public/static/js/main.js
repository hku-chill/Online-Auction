// $(document).on("click touch",".tc_valide_button", e=> {
//     e.preventDefault();
//     console.log(e);
//     return false;
// });

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