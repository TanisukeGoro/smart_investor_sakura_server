<?php
?>
@extends('layouts.app')
@section('content')

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <link href="{{ asset('css/reset.css') }}" rel="stylesheet" >
    <link href="{{ asset('css/serch_reslt.css') }}" rel="stylesheet">
    <title>Document</title>
</head>
<body>
    <div class="mein">
        <p class="mein_title">企業名検索結果一覧</p>
        <table>
            <tr>
                <td>銘柄コード</td>
                <td>企業名</td>
                <td>市場</td>
                <td>項目</td>
                <td>項目</td>
                <td>項目</td>
            </tr>
            <tr>
                <td>1234</td>
                <td>総合商社タニケン</td>
                <td>マザーズ</td>
                <td>項目</td>
                <td>項目</td>
                <td>項目</td>
            </tr>
            <tr>
                <td>5678</td>
                <td>タニケンカンパニーズ</td>
                <td>東証1部</td>
                <td>項目</td>
                <td>項目</td>
                <td>項目</td>
            </tr>
            <tr>
                <td>9112</td>
                <td>あべソリューションズ</td>
                <td>東証2部</td>
                <td>項目</td>
                <td>項目</td>
                <td>項目</td>
            </tr>
        </table>
    </div>
    <div class="footer">

    </div>
</body>
</html>
@endsection