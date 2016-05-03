var $jq = jQuery.noConflict();
$jq('.checkbox-main:checkbox').change(function () {
    $jq(".checkbox-sub-"+$jq(this).val()).prop("checked", $jq(this).is(':checked'));
});
