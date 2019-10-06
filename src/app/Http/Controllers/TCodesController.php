<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\CompanyInfo;
use App\Favorite;
use App\FinancialReport;

use Validator;

class TCodesController extends Controller
{
    public function __construct()
    {
        $this->middleware('auth');
    }
    // 🐽index用、未作成🐽
    public function index()
    {
        return view('welcome'); // 仮でページ遷移
    }

    // 🐽main用、未作成🐽
    public function main()
    {

        $financial_reports = new FinancialReport();
        $result = $financial_reports->getData();
        return view('main', [
            'roe_reports' => $result
        ]);
    }

    // 🐽search用、未作成🐽
    public function search()
    {
        return view('search'); // 仮でページ遷移
    }

    // 🐽company用、未作成🐽
    public function company($edintCode)
    {
        $company_infos = new CompanyInfo();
        $result = $company_infos->getData($edintCode);
        $roe = $company_infos->getFinancaldata($edintCode);
        return view('company', [
            'campany_info' => $result,
            'roe' => $roe
        ]); // 仮でページ遷移
    }

    // 🐽my_account用、未作成🐽
    public function account()
    {
        // public function account(Request $request) {
        // return view('my_account'); // 仮でページ遷移

        // バリデーション
        // $validator = Validator::make($request->all(), [
        //     'item_name' => 'required | max:255',
        //     'item_number' => 'required | min:1 | max:3',
        //     'item_amount' => 'required | max:6',
        //     'published' => 'required',
        // ]);
    }

    // 🐽my_activity用、未作成 なので、現在はエラーとなっていて、mainへ遷移するようにしている🐽
    // public function activity() {
    public function activity(Request $request)
    {

        // バリデーション
        $validator = Validator::make($request->all(), [
            'name' => 'required | max:255',
            'company_id' => 'required | max:255',
            'stock_code' => 'required | min:1 | max:3',
            'listing_category' => 'required | max:6',
        ]);

        //バリデーション:エラー
        if ($validator->fails()) {
            return redirect('/main')
                ->withInput()
                ->withErrors($validator);
        }
        //以下に登録処理を記述（Eloquentモデル）
        // Eloquent モデル
        $favorites = new Favorite;
        $favorites->name = $request->name;
        $favorites->company_id = $request->company_id;
        $favorites->stock_code = $request->stock_code;
        $favorites->listing_category = $request->listing_category;
        $favorites->save();
        return redirect('/my_activity');
    }
}
