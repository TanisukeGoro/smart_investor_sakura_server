<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateFinancialReportsTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('financial_reports', function (Blueprint $table) {
            $table->increments('id');
            $table->float('Bonds', 15, 0);
            $table->float('CP', 15, 0);
            $table->float('Capex', 15, 0);
            $table->float('CashEquivalents', 15, 0);
            $table->float('Depreciation', 15, 0);
            $table->float('GrossProfit', 15, 0);
            $table->float('Inventories', 15, 0);
            $table->float('NetAssets', 15, 0);
            $table->float('NetSales', 15, 0);
            $table->float('OperatingProfit', 15, 0);
            $table->float('OrdinaryIncomeLoss', 15, 0);
            $table->integer('ParseFlg');
            $table->float('ProfitLoss', 15, 0);
            $table->float('ROE', 10, 4);
            $table->integer('RequestFlg');
            $table->float('ShareholdersEquity', 15, 0);
            $table->float('Valuation', 15, 0);
            $table->float('acPayable', 15, 0);
            $table->float('acReceivable', 15, 0);
            $table->float('cfFinancing', 15, 0);
            $table->float('cfInvesting', 15, 0);
            $table->float('cfOperating', 15, 0);
            $table->float('cpBonds', 15, 0);
            $table->float('cpLoans', 15, 0);
            $table->integer('disclosureStatusFlg');
            $table->string('docID');
            $table->string('edinetCode');
            $table->string('filerName');
            $table->float('ltLoans', 15, 0);
            $table->float('psBasicEarningsLoss', 15, 0);
            $table->float('psNetAssets', 15, 0);
            $table->integer('season');
            $table->string('series_data');
            $table->float('stBonds', 15, 0);
            $table->float('stLoans', 15, 0);
            $table->float('tAssets', 15, 0);
            $table->float('tIssuedShares', 15, 0);
            $table->integer('xbrlFlg');
            $table->integer('year'); // 40

            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('financial_reports');
    }
}
