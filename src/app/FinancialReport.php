<?php

namespace App;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Facades\DB;
use Symfony\Component\VarDumper\VarDumper;

class FinancialReport extends Model
{
    protected $table = 'financial_reports';
    protected $guarded = array('business_category');
    public $timestamps = false;

    public function getData()
    {
        $data = DB::select('SELECT DISTINCT year, edinetCode, ROE 
                            FROM financial_reports 
                            WHERE xbrlFlg != 444 
                            AND RequestFlg !=444 
                            AND ParseFlg!=444 
                            AND disclosureStatusFlg != 444 
                            ORDER BY edinetCode , year ASC');

        $results = $this->selectCompanyByROE($data);
        $query_code = [];
        // Sort
        foreach ((array) $results as $key => $value) {
            $sort[$key] = $value['aveROE'];
            $query_code[] = $value['edinetCode'];
        }
        array_multisort($sort, SORT_DESC, $results);

        // Create SQL 
        $sql = 'SELECT * FROM company_infos WHERE edinet_code IN ("' . implode('","', $query_code) . '");';
        $company_info = $this->getCampanyName($sql);
        $output = [];
        foreach ((array) $results as $key => $value) {
            foreach ($company_info as $key2 => $value2) {
                if ($value['edinetCode'] == $value2->edinet_code) {
                    // var_dump($value["edinetCode"], $value2->edinet_code);
                    $tmpArr = array(
                        'aveROE' =>  $value["aveROE"],
                        'years' => $value["years"],
                        'edinetCode' => $value["edinetCode"],
                        'listingCategory' => $value2->listing_category,
                        'closing_date' => $value2->closing_date,
                        'name' => $value2->name,
                        'business_category' => $value2->business_category,
                        'stock_code' => $value2->stock_code,
                    );
                    $output[] = $tmpArr;
                }
            }
        }
        $category_info = DB::select('SELECT * FROM category_infos');
        foreach ($output as $key => $value) {
            foreach ($category_info as $key2 => $value2) {
                if ($value['business_category'] == $value2->business_category) {
                    // var_dump($value["edinetCode"], $value2->edinet_code);
                    $output[$key]["business_category"] = $value2->business_category_name;
                }
            }
        }
        // 順番に並び替える
        return $output;
    }
    public function selectCompanyByROE($data)
    {
        $tmp_code = $data[0]->edinetCode;
        $sum_roe = 0;
        $tmp_count = 0;

        $results = [];

        $roe_flg = true;
        $count = count($data);

        for ($j = 0; $j < $count; $j++) {
            if ($tmp_code != $data[$j]->edinetCode) {
                if ($roe_flg && $tmp_count >= 9) {
                    // 追加
                    $resultObj = array(
                        'aveROE' => $sum_roe / $tmp_count,
                        'years' => $tmp_count,
                        'edinetCode' => $tmp_code
                    );
                    $results[] = $resultObj;
                }
                // var_dump($results);

                // 初期化
                $sum_roe = 0;
                $tmp_count = 0;
                $tmp_code = $data[$j]->edinetCode;
                $roe_flg = true;
            }


            if (!$roe_flg) {
                continue;
            }

            $sum_roe = $sum_roe + $data[$j]->ROE;
            $tmp_count++;

            if ($data[$j]->ROE < 0.15) {
                $roe_flg = false;
            }

            // unset($data[$j]);

        }
        return $results;
    }
    public function getCampanyName($queyr_code)
    {
        return DB::select($queyr_code);
    }
}
