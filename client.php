/**
  * socket client
  * a NULL填充字符串
  * n 表式无符号短整形
  * 无符号短整型, 总是16点，大端字节序
  */
function insert_queue($cmd, $sql) {
    $s = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
    try {
      socket_connect($s, "127.0.0.1", 8888);
      $list = json_encode(array(
        "sql"=>$sql
      ));
      $len = strlen($list);
      $param = pack("nna{$len}",$cmd, $len, $list);
      socket_write($s, $param, strlen($param));
      socket_recv($s, $head, 4, 0);
      //var_dump($head);
      if($head != '') {
        $a = unpack("ncmd/nlen", $head);
        $cmd = $a['cmd'];
        $len = $a['len'];
        if($cmd == 8001) {
          socket_recv($s, $body, $len, 0);
          //echo $body;exit;
          $b = json_decode($body, true);
          socket_close($s);
          return $b;
        }
      }
      socket_close($s);
    } catch(Exception $e) {
      echo $e->getMessage();
    }
}
$temp = insert_queue(8001, "insert into (num) values (%d)");
