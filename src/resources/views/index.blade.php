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
    <link href="{{ asset('css/lp.css') }}" rel="stylesheet">
    <title>Taniken Code</title>
</head>
<body>
    <div class="header_img_aria">
        <div class="img_text_aria">
            <p class="img_text">
            バリュー投資を行うために必要な<br>
            情報は全てここにあります。
            </p>
        </div>
    </div>
    <div class="mein01">
        <p class="mein01_text">
                <b>煩雑な分析作業に辟易していませんか？</b><br>
                企業分析をしようとしたとき、これまではいくつものハードルがありました。<br>
                <br>
                たとえばあるA社について情報収集をする場合。<br>
                まず株価サイトでA社の株価を確認して、<br>
                次にA社のIRページから有価証券報告書や決算短信をダウンロードして、<br>
                エクセルを開いて必要な数字をコピペして、<br>
                そしてようやく財務指標を計算したり数字を並べて比較したりしていましたよね。<br>                
        </p>
        <img class="mein01_img" src="img/mein01_img.jpg" alt="">
    </div>
    <div class="mein02">
        <img class="mein02_img" src="img/mein02_img.jpg" alt="">
        <p class="mein02_text">
                <b>Smart Investorが解決</b><br>
                Smart Investorは、そうした煩雑な作業を<br>
                あなたに代わって一瞬で行います。<br>
                <br>
                もうあちこちのサイトを飛び回って数字<br>
                をコピペする必要はありません。<br>
                有利子負債もEBITDAも、面倒なROEの<br>
                デュポン分解も、<br>
                私たちが必要な数字を集めて計算し、<br>
                見やすく表示します。<br>
                <br>
                必要な情報はすべてここにあります。<br>
        </p>
    </div>
    <div class="mein03">
        <p class="mein03_title">煩わしい情報集めにサヨナラ。企業分析がもっと迅速・カンタンに。</p>
        <p class="mein03_text01">
                企業分析に必要な情報が豊富にそろうSmart Investorなら、<br>
                煩わしい情報集めの負担を軽くし、迅速な分析への近道が見つかります。<br>
                <br>
                世界一の投資家、ウォーレン・バフェットだけ見えている黄金の投資法則を<br>
                探してみませんか？<br> 
        </p>
        <p class="mein03_text02"><a href="#">>>さっそく使ってみる！(無料）</a></p>
    </div>
    <div class="mein04">
        <div class="mein04_text_aria">
            <div class="mein04_title_aria">
                <img class="mein04_title_img" src="img/musimegane_img.png" alt="検索">
                <p class="mein04_title_text">検索（Search）</p>
            </div>
            <p class="mein04_text">
                    <b>様々な情報ソースへのアクセスを不要に</b><br>
                    これからはSmart Investorで検索するだけ。<br>
                    財務データ・株価データなど、本来であれば、多様な情報ソースを活用しなければ取得できない情報が全てA社のページに掲載されています。<br>
                    PERやEV/EBITDA、ROEのデュポン分解といった指標も多数掲載しています。<br>
            </p>
        </div>
        <img class="mein04_img" src="img/mein04_img.jpg" alt="検索">
    </div>
    <div class="mein05">
        <img class="mein05_img" src="img/mein05_img.jpg" alt="見つける">
        <div class="mein05_text_aria">
            <div class="mein05_title_aria">
                <img class="mein05_title_img" src="img/roto_img.jpg" alt="見つける">
                <p class="mein05_title_text">条件検索</p>
            </div>
            <p class="mein05_text">
                    <b>投資方針にマッチする企業を見つけよう</b><br>
                    上場企業約3,600社の中からご希望の財務指標で絞り込むことができます。<br>
                    スクリーニングに使える指標は売上高、ROEなど30種類以上！<br>
                    あなたの投資方針にマッチする上場企業がきっと見つかります。<br>
            </p>
        </div>
    </div>
    <div class="mein06">
        <div class="mein06_title_aria">
            <p class="mein06_title">収録コンテンツ</p>
        </div>
        <div class="mein06_text">
            <div class="mein06_text01">
                <p class="mein06_text01_title">掲載企業数</p>
                <p>国内上場企業（約3,700社)</p>
            </div>
            <div class="mein06_text02">
                <p class="mein06_text02_title">収録データ</p>
                <p class="mein06_list">
                        1. 会社概要（事業内容など）<br>
                        2. 財務指標（ROE、有利子負債、配当利回り）<br>
                        3. 詳細財務（B/S、P/L、C/F）<br>
                </p>
            </div>
        </div>
        <div class="mein06_footer_aria">
            <p class="mein06_footer_text01">
                収録している財務数値は、金融庁が一般公開しているEDINETシステムから取得しております。
            </p>
            <p class="mein06_footer_link"><a href="#">>>さっそく使ってみる！</a></p>
        </div>
        <div class="mein07">
            <div class="mein07_text_aria">
                <p class="mein07_text">
                    お問い合わせ<br>
                </p>
            </div>
        </div>
    </div>
    <div class="footer_aria">
        <ul class="footer_list">
            <li><a href="#">開発について</a></li>
            <li><a href="#">利用規約</a></li>
            <li><a href="#">お問い合わせ</a></li>
        </ul>
    </div>
</body>
</html>
@endsection  
