<!DOCTYPE html>
<html lang="{{ app()->getLocale() }}">

<head>
    <!--ヘッダー -->
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- CSRF Token -->
    <meta name="csrf-token" content="{{ csrf_token() }}">

    <title>{{ config('app.name', 'Laravel') }}</title>

    <!-- Styles -->
    <link href="{{ asset('css/app.css') }}" rel="stylesheet">
    <link href="{{ asset('css/my_activity.css') }}" rel="stylesheet">
</head>

<body style="padding-top:4.5rem;">
    <div id="app">
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
            <div class="container">
                <!-- Branding Image -->
                <a class="navbar-brand" href="{{ url('/') }}">
                    <img src="{{ asset('master_favicon_opasity.png') }}" width="30" height="30" class="d-inline-block align-top" alt="ブランド">
                    {{ config('app.name', 'Laravel') }}
                </a>

                <div class="collapse navbar-collapse" id="navbarNavDropdown">

                    <!-- この下の行に mr-auto クラスを付与するだけ -->
                    <ul class="navbar-nav mr-auto">　
                        <li class="nav-item">
                            <a class="nav-link" href="{{url('/main')}}">ROE上位企業一覧</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#">詳細検索</a>
                        </li>
                    </ul>

                    <ul class="navbar-nav">
                        <!-- Authentication Links -->
                        @guest
                        <li class="nav-item">
                            <a class="nav-link" href="{{ route('login') }}">
                                Login
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ route('register') }}">
                                Register
                            </a>
                        </li>
                        @else
                        <li class="nav-item dropdown">
                            <a href="#" class="dropdown-toggle nav-link" data-toggle="dropdown" role="button" aria-expanded="false" aria-haspopup="true" v-pre>
                                {{ Auth::user()->name }} <span class="caret"></span>
                            </a>

                            <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                                <li>
                                    <a class="dropdown-item" href="{{ route('logout') }}" onclick="event.preventDefault();
                            document.getElementById('logout-form').submit();">
                                        Logout
                                    </a>

                                    <form id="logout-form" action="{{ route('logout') }}" method="POST" style="display: none;">
                                        {{ csrf_field() }}
                                    </form>
                                </li>
                            </ul>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ route('logout') }}" onclick="event.preventDefault();
                            document.getElementById('logout-form').submit();">
                                Logout
                            </a>
                        </li>
                        @endguest

                        <div class="collapse navbar-collapse" id="navbarForm">
                            <form class="form-inline my-2 my-lg-0 ml-auto" action="" method="POST">
                                <input class="form-control mr-sm-2" type="text" placeholder="検索..." aria-label="企業検索...">
                                <button type="submit" class="btn btn-outline-success my-2 my-sm-0">検索</button>
                            </form>
                        </div>
                    </ul>

                </div>
            </div>
        </nav>

    </div>

    @if(Request::is('/'))
    @else
    @guest

    @else
    <div class="container-fluid">
        <div class="row">
            <nav class="col-md-2 d-none d-md-block bg-light sidebar">
                <div class="sidebar-sticky mt-4">
                    <ul class="nav flex-column">
                        <li class="nav-item">
                            <a class="nav-link " href="{{ url('/main') }}">
                                <span data-feather="home"></span>
                                スクリーニング <span class="sr-only">(現位置)</span>
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#">
                                <span data-feather="shopping-cart"></span>
                                お気に入り
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#">
                                <span data-feather="bar-chart-2"></span>
                                有価証券報告書一覧
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#">
                                <span data-feather="layers"></span>
                                統合
                            </a>
                        </li>

                    </ul>

                    <h6 class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-muted">
                        <span>保存されたレポート</span>
                        <a class="d-flex align-items-center text-muted" href="#">
                            <span data-feather="plus-circle"></span>
                        </a>
                    </h6>
                    <ul class="nav flex-column mb-2">
                        <li class="nav-item">
                            <a class="nav-link" href="#">
                                <span data-feather="file-text"></span>
                                今月
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#">
                                <span data-feather="file-text"></span>
                                前四半期
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#">
                                <span data-feather="file-text"></span>
                                社会的関与
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#">
                                <span data-feather="file-text"></span>
                                資産
                            </a>
                        </li>
                    </ul>
                </div>
            </nav>
        </div>
    </div>
    @endguest
    @endif
    @yield('content')

    </div>

    <!-- Scripts -->
    <script src="{{ asset('js/app.js') }}"></script>
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous">
    </script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.bundle.min.js" integrity="sha384-xrRywqdh3PHs8keKZN+8zzc5TX0GRTLCcmivcbNJWm2rs5C8PRhcEn3czEjhAO9o" crossorigin="anonymous">
        //JavaScriptプラグインの設定など
    </script>
    <!-- アイコン -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/feather-icons/4.9.0/feather.min.js"></script>
    <script>
        feather.replace()
    </script>
</body>

</html>