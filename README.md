[discord.py]: https://github.com/Rapptz/discord.py
[discord-ext-menus]: https://github.com/Rapptz/discord-ext-menus
[dispander]: https://github.com/DiscordBotPortalJP/dispander
[pyyaml]: https://github.com/yaml/pyyaml
[dataclasses]: https://docs.python.org/ja/3/library/dataclasses.html

# TL;DR

bot用の便利関数などをまとめたパッケージのリポジトリです。
個人的に便利で複数のBOTで利用するであろう機能をまとめています。

# 機能

以下アルファベット順に。

## blacklist

以下のdata管理機能を利用した機能制限システムです。discord bot内の一部機能の使用制限に用いることを想定しています。

## config

ビルトインパッケージの[dataclasses]を利用したconfig管理機能です。configは自動的にカレントディレクトリの`config.yaml`に保存されます。

使用例
```py
from dataclasses import dataclass
from bot_util.config import config, ConfigBase

@dataclass
class MyBotSetting(ConfigBase):
    sending_channel_id: int= None

config.add_default_config(MyBotSetting, key='setting')
print(config.setting)
#MyBotSetting(sending_channel_id=None)
```

## context

[discord.py]のContextに、エラー処理済みの属性と、いくつかの便利関数を追加した子クラスです。

## data

[dataclasses]と[yaml][pyyaml]を利用したdata管理機能です。dataはカレントディレクトリの`data`フォルダの`.yaml`または、`.yml`から読み込まれます。

## dispander

[dispander]をもとに改変を加えています。使い方は変化していないので、
[dispander]を参照してください。

### originalからの変更点

- cogとしての機能を削除
- 送信を決める対象を変更(bug?)
- 埋め込みのcolorを指定(configで変更可能)

## help_command

BOTのヘルプを表示するためのクラスが記述されています。BOT定義時に呼び出して、インスタンスを渡すことで利用可能です。埋め込みのcolorをconfigから指定できます。

## menus

[discord-ext-menus]のクラスをもとに、メッセージ送信時も特定の関数が呼び出されるようなクラスを用意し、discord.ext.menusの全てをimportしています。

| original class | message ver |
|---|---|
| Menu | MsgMenu |
| MenuPages | MsgMenuPages |

## sio client

開発中です。 </br>
minecraftとの通信専用のsocketIOのクライアントを実装中です。

## util

便利関数などがあります。以下は一覧です。

### YAML_DUMP_CONFIG

自分がよく使うdump時の設定のまとめです。

### split_line

`string`を`num`で指定した文字数で分割して`list`にして返します。主に`embed`の`field`分割用です。

Parameters
string: `str`
    分割元の文字列です。
num: `int`
    分割したい最大の文字列です。

Returns
llist\[str]
    分割された文字列です。

### get_unique_list

名前の通り、重複の含まれる`list`を順番を保持して一意な要素にします。
`need_flatten`を`True`にすると、二次元配列を一次元配列にして一位な要素が含まれる`list`にします。

Parameters
not_unique_list: `list`
    一意な要素のlistにしたいlistです。
need_flatten: `bool`
    Trueにすると、二次元配列を一次元配列にして一意な要素にします。

Returns
`list`
    一意な要素のlistです。

### TimestampStyle

`type hint`です。

### format_dt

discordの時間表記にするためのユーティリティ関数です。

Parameters
dt: `datetime.datetime`
    The datetime to format.
style: `str`
    The style to format the datetime with.

Returns
`str`
    The formatted string.

## wraped embed

discord.Embedに文字数チェックと、関数アノテーションをつけた子クラスです。

# 利用しているパッケージ

- [discord.py]
- [discord-ext-menus]
- [dispander]
- [pyyaml]
