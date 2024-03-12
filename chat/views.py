from django.shortcuts import render
from django.http import HttpResponse
#from .duplicate_project import *
from .duplicate_project_output import chat

TEMPLATE_STRING = '''<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

    <title>Hello, world!</title>
    <script>
        $(document).ready(function(){
          $("button").click(function(){
            username = $('#username').val()
            base_url = '/bot/'
            main_url = base_url.concat(username)
            console.log(main_url)
            $.ajax({
            url: main_url,
            cache: false,
            success: function(html){
                if (html == 'Entire 3rd floor belongs to fashion and clothings')
                {
                    $("#result").html("<h3 class='text-center mt-5 disp-5'>Sorry, I didn't get that. Try Again</h3>");
                }
                else{
                    $("#result").html("<h3 class='text-center mt-5 disp-5'>" + html + "</h3>");
                }
                $("#result").show(1000);
                $("#result").delay(3000).hide(500);
                $('input:text').delay(3000).val('');
            },
            error: function (request, status, error) {
              $("#result").html('<h5 class="text-center text-danger bg-warning">No records found for the given username</h5>');
      }
  });
          });
        });
      </script>
  </head>
  <body class='bg-light'>
<div class="container">
  <div class="height container-fluid">
    <h1 style="height: 10vh; background-color:#b0f7e3;" class='text-center mt-5'>Tata Consultancy Services<br><br> TCS Mart</h1>
    <div class="form-group" style='margin-top: 100px;' >
        <div class="input-group  rounded-pill">
          <input type="text" name="username" id='username' class='form-control form-control-lg  border-warning' size='30' placeholder="How can I help you?" style='border-width: 2px;!important border-style: solid;'>
          <div class="input-group-append">
            <button  value='Search' id='search' class='btn btn-warning'>
              <div class="text-dark font-weight-bold">
                Search
              </div>
            </button>
          </div>
        </div>
      </div>
    <div id="result"></div>
  </div>
  </div>
    

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
  </body>
</html>'''

# Create your views here.
def chat_intro_view(request):
    return HttpResponse(TEMPLATE_STRING)

def chat_view(request, query=None):
    output = chat(query)
    return HttpResponse(output)

