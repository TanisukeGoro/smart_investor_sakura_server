<?php

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

// モデル作成済
use App\CompanyInfo;
use App\Favorite;
use App\FinancialReport;
use Illuminate\Http\Request;

// 🐽下記 TCodesController.phpへ。indexページ作成しただけ🐽
// index(LP)用。
// Route::get('/', 'TCodesController@index');
Route::get('/', function () {
    return view('welcome');
});


// 🐽下記 TCodesController.phpへ。mainページ作成しただけ🐽
// main用。
Route::get('/main', 'TCodesController@main');

// 🐽下記 TCodesController.phpへ。searchページ作成しただけ🐽
// search用。
Route::get('/search', 'TCodesController@search');

// 🐽下記 TCodesController.phpへ。companyページ作成しただけ🐽
// company用。
Route::get('/company/{edintCode}', 'TCodesController@company');

// MyAccount への登録
// 🐽登録なので後から post に変更する🐽
// 🐽下記 TcodesController.phpへ。my_account ページ作成しただけ🐽
Route::get('/my_account', 'TCodesController@account');

// MyActivity への登録
// 🐽登録なので後から post に変更する🐽
// 🐽下記 TcodesController.phpへ。my_activity ページ作成しただけ🐽
Route::get('/my_activity', 'TCodesController@activity');




// Auth::routes();

// Route::get('/my_activity', 'HomeController@index')->name('home');

Auth::routes();

Route::get('/main', 'TCodesController@main')->name('main');
