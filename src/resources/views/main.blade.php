<?php

// echo "ここが main ページ。web.phpで定義👉TCodesController.php に処理";
// Debugbar::info($roe_reports);
?>

@extends('layouts.app')
@section('content')

<main role="main" class="col-md-10 ml-sm-auto col-lg-10 px-4">
  <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
    <h1 class="h2">優良ROE企業</h1>
    <p>過去10年間毎年ROE(自己資本利益率)が15%以上の企業
    </p>
    <div class="btn-toolbar mb-2 mb-md-0">
      <div class="btn-group mr-2">
        <button type="button" class="btn btn-sm btn-outline-secondary">上場</button>
        <button type="button" class="btn btn-sm btn-outline-secondary">非上場</button>
      </div>
      <button type="button" class="btn btn-sm btn-outline-secondary dropdown-toggle">
        <span data-feather="calendar"></span>
        期間選択
      </button>

    </div>

  </div><!-- /.table-responsive -->

  <div class="table-responsive">
    <table class="table table-striped table-sm">
      <thead>
        <tr>
          <th>平均ROE</th>
          <th>企業名</th>
          <th>証券コード</th>
          <th>事業</th>
          <th>市場</th>
          <th>開示資料</th>
        </tr>
      </thead>
      <tbody>
        @foreach($roe_reports as $financial_report)
        <tr>
          <td> {{ round($financial_report["aveROE"] *100,1)}} %</td>
          <td><a href='/company/{{$financial_report["edinetCode"]}}'>{{ $financial_report["name"]}}</a></td>
          <td><a href="">{{ $financial_report["stock_code"]}}</a></td>
          <td><a href="">{{ $financial_report["business_category"]}}</a></td>
          <td>{{ $financial_report["listingCategory"]}}</td>
          <td><a href="#">開示資料</a></td>
        </tr>
        @endforeach
      </tbody>
    </table>
  </div>
</main>
@endsection