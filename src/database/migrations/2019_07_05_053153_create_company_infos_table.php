<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateCompanyInfosTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('company_infos', function (Blueprint $table) {
            $table->increments('id');
            $table->string('edinet_code');
            $table->string('listing_category');
            $table->string('closing_date');
            $table->string('name');
            $table->string('name_en');
            $table->string('name_kana');
            $table->integer('business_category');
            $table->integer('stock_code');
            $table->float('company_id', 15, 0);
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
        Schema::dropIfExists('company_infos');
    }
}
