<?php
// use DebugBar\DebugBar;

// // echo "ここが company ページ。web.phpで定義👉TCodesController.php に処理";

// Debugbar::info($campany_info);
$roe_value = [];
$psNetasset = [];
foreach ((array) $roe as $value) {
    $roe_value[] = $value->ROE * 100;
    $psNetasset[] = $value->psNetAssets;
}
// Debugbar::info(implode(',', $roe_value));

?>

@extends('layouts.app')
@section('content')

<main role="main" class="col-md-10 ml-sm-auto col-lg-10 px-4">
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
        <h1 class="h2">{{$campany_info[0]->name}}</h1>
        <div class="btn-toolbar mb-2 mb-md-0">
            <button type="button" class="btn btn-sm btn-outline-secondary dropdown-toggle">
                <span data-feather="calendar"></span>
                期間選択
            </button>

        </div>

    </div><!-- /.table-responsive -->
    <div class="row sampleRowB">
        <div class="col-md-8">
            <h2>ROEおよび一株あたりの利益率</h2>
            <canvas class="my-4 w-100" id="financeChart" width="400" height="180"></canvas>
        </div>
        <div class="col-md-4">
            <h2>企業概要</h2>
            <div class="table-responsive">
                <table class="table table-striped table-sm">
                    <thead>
                        <tr>
                            <th></th>
                            <th>内容</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>EDINETコード</td>
                            <td>{{$campany_info[0]->edinet_code}}</td>
                        </tr>
                        <tr>
                            <td>決算日</td>
                            <td>{{$campany_info[0]->closing_date}}</td>
                        </tr>
                        <tr>
                            <td>証券コード</td>
                            <td>{{$campany_info[0]->stock_code}}</td>

                        </tr>
                        <tr>
                            <td>事業内容</td>
                            <td>{{$campany_info[0]->business_category}}</td>

                        </tr>
                        <tr>
                            <td>法人番号</td>
                            <td>{{$campany_info[0]->company_id}}</td>
                        </tr>
                    </tbody>
                </table>

            </div>
        </div>

        <div class="syumi-aria" style="padding-left: 60px;padding-right: 60px;padding-top: 60px;">
            <p class="syumi-title" style="font-size: 35px;border-left: 10px solid #24a045;padding-left: 10px;">企業価値シュミレーション</p>
            <p class="syumi-text01" style="font-size:25px;">企業価値を試算してみましょう。</p>
            <div style="display: flex;height: 30px;margin-bottom: 20px;" class="syumi-text02-aria">
                <p class="syumi-text02" style="font-size:18px;padding-right: 10px;">現在から5年後までのCFの成長率</p>
                <input type="text" value="15">
                <p style="font-size: 25px;padding-top: 0px;margin-left: 10px;">%</p>
            </div>
            <div style="display: flex;height: 30px;" class="syumi-text03-aria">
                <p class="syumi-text03" style="font-size: 20px;padding-right: 10px;">それ以降</p>
                <input type="text" value="10">
                <p style="font-size: 20px;padding-top: 0px;margin-left: 10px;">%</p>
                <a href="#" class="btn btn-info" style="margin-left: 35px;padding-top: 3px;padding-left: 15px;padding-right: 15px;">試算 -></a>
            </div>
            <img style="width: 900px;margin-top: 100px;margin-left: 170px;" src="img/grf_img.jpg" alt="">
        </div>
    </div>
    <div class="row sampleRowB">
        <div class="col-md-6">
            <h2>理論株価シミュレーション結果</h2>
            <div class="table-responsive">
                <table class="table table-striped table-sm">
                    <thead>
                        <tr>
                            <th>理論株価</th>
                            <th>¥ 1230,0 円</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>現在株価</td>
                            <td>¥ 920,4 円</td>
                        </tr>

                    </tbody>
                </table>
            </div>
        </div>
        <div class="col-md-6">
            <h2>企業価値シミュレーションチャート</h2>
            <div>
                <a href="https://plot.ly/~TanisukeGoro/391/?share_key=MnBXBHheBZgJsTd8Rl1w67" target="_blank" title="Plot 391" style="display: block; text-align: center;"><img src="https://plot.ly/~TanisukeGoro/391.png?share_key=MnBXBHheBZgJsTd8Rl1w67" alt="Plot 391" style="max-width: 100%;width: 600px;" width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
                <script data-plotly="TanisukeGoro:391" sharekey-plotly="MnBXBHheBZgJsTd8Rl1w67" src="https://plot.ly/embed.js" async></script>
            </div>

        </div>
    </div>

</main>

<!-- グラフ -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.3/Chart.min.js"></script>
<script>
    window.onload = function() {
        var complexChartOption = {
            responsive: true,
            scales: {
                yAxes: [{
                    id: "y-axis-1", // Y軸のID
                    type: "linear", // linear固定 
                    position: "left", // どちら側に表示される軸か？
                    // ticks: { // スケール
                    //     max: 0.2,
                    //     min: 0,
                    //     stepSize: 0.1
                    // },
                }, {
                    id: "y-axis-2",
                    type: "linear",
                    position: "right",
                    // ticks: {
                    //     max: 1.5,
                    //     min: 0,
                    //     stepSize: .5
                    // },
                    gridLines: { // このオプションを追加
                        drawOnChartArea: false,
                    },
                }],
            }
        };

        var barChartData = {
            labels: ["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018"],
            datasets: [{
                    type: 'line', // 追加
                    label: 'ROE [ % ]',
                    data: [<?= implode(',', $roe_value) ?>],
                    // borderColor: "rgba(254,97,132,0.8)",
                    pointBackgroundColor: "rgba(254,97,132,0.8)", // 追加
                    fill: false, // 追加
                    backgroundColor: "rgba(254,97,132,0.5)",
                    yAxisID: "y-axis-1", // 追加
                },
                {
                    type: 'bar', // 追加
                    label: '一株あたりの利益 [ 円 ]',
                    data: [<?= implode(',', $psNetasset) ?>],
                    borderColor: "rgba(54,164,235,0.8)",
                    backgroundColor: "rgba(54,164,235,0.5)",
                    yAxisID: "y-axis-2", // 追加
                },
            ],
        };

        ctx = document.getElementById("financeChart").getContext("2d");
        window.myBar = new Chart(ctx, {
            type: 'bar', // ここは bar にする必要があります
            data: barChartData,
            options: complexChartOption
        });
    };
</script>


@endsection