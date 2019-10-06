<?php

namespace App;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Facades\DB;

class CompanyInfo extends Model
{
    public function getData($edinetCode)
    {
        $sql = 'SELECT * FROM company_infos WHERE  edinet_code=' . "'" . $edinetCode . "'";
        $infomation = DB::select($sql);
        $category_info = DB::select('SELECT * FROM category_infos');
        foreach ($category_info as $key2 => $value2) {
            if ($infomation[0]->business_category == $value2->business_category) {
                // var_dump($value["edinetCode"], $value2->edinet_code);
                $infomation[0]->business_category = $value2->business_category_name;
            }
        }
        return $infomation;
    }
    public function getFinancaldata($edinetCode)
    {
        $sql = ('SELECT DISTINCT year, edinetCode, ROE,  psNetAssets
                            FROM financial_reports 
                            WHERE xbrlFlg != 444 
                            AND RequestFlg !=444 
                            AND ParseFlg!=444 
                            AND disclosureStatusFlg != 444 
                            AND edinetCode=' . "'" . $edinetCode . "'" . '
                            ORDER BY edinetCode , year ASC');

        return DB::select($sql);
    }
}
