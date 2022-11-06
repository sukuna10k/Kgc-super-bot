# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import io
import sys
import os
import traceback
import asyncio
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from info import COMMAND_HANDLER
from bot import app

__MODULE__ = "DevCommand"
__HELP__ = """
**For Owner Bot Only.**
/run [args] - Run eval CMD
/shell [args] - Run Exec/Terminal CMD
/download [link/reply_to_telegram_file] - Download file from Telegram

**For Public Use**
/json - Send structure message Telegram using Pyrogram Style.
"""

@app.on_message(filters.command(["donate"], COMMAND_HANDLER))
async def donate(_, message):
    markup = InlineKeyboardMarkup([[InlineKeyboardButton("Dana", url="https://link.dana.id/qr/3kqod34"), InlineKeyboardButton("ShopeePay", url="https://wsa.wallet.airpay.co.id/qr/00c06de2ee3d0c7169e8?smtt=0.0.9")]])
    await message.reply(f"Hai {message.from_user.mention}, jika kamu merasa bot ini berguna bisa melakukan donasi dengan payment yang tersedia untuk kebutuhan server dan lainnya. Terimakasih..", reply_markup=markup)

@app.on_message(filters.command(["balas"], COMMAND_HANDLER) & filters.user([617426792, 2024984460]) & filters.reply)
async def balas(c, m):
    pesan = m.text.split(" ", 1)
    await m.delete()
    await m.reply(pesan[1], reply_to_message_id=m.reply_to_message.id)


@app.on_message(filters.command(["neofetch"], COMMAND_HANDLER) & filters.user(617426792))
async def neofetch(c, m):
    neofetch = (await shell_exec("neofetch --stdout"))[0]
    await m.reply(f"<code>{neofetch}</code>", parse_mode=enums.ParseMode.HTML)


@app.on_message(filters.command(["shell", "sh"], COMMAND_HANDLER) & filters.user([617426792, 2024984460]))
@app.on_edited_message(filters.command(["shell", "sh"], COMMAND_HANDLER) & filters.user([617426792, 2024984460]))
async def shell(client, message):
    cmd = message.text.split(" ", 1)
    if len(cmd) == 1:
        return await message.reply("No command to execute was given.")
    shell = (await shell_exec(cmd[1]))[0]
    if len(shell) > 3000:
        with open("shell_output.txt", "w") as file:
            file.write(shell)
        with open("shell_output.txt", "rb") as doc:
            await message.reply_document(document=doc, file_name=doc.name)
            try:
                os.remove("shell_output.txt")
            except:
                pass
    elif len(shell) != 0:
        await message.reply(shell, parse_mode=enums.ParseMode.HTML)
    else:
        await message.reply("No Reply")


@app.on_message(filters.command(["ev", "run"]) & filters.user([617426792, 2024984460]))
@app.on_edited_message(filters.command(["ev", "run"]) & filters.user([617426792, 2024984460]))
async def evaluation_cmd_t(client, message):
    status_message = await message.reply("__Processing eval pyrogram...__")
    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await status_message.edit("__No evaluate message!__")
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"

    final_output = f"**EVAL**:\n`{cmd}`\n\n**OUTPUT**:\n`{evaluation.strip()}`\n"

    if len(final_output) > 4096:
        with open("MissKatyEval.txt", "w+", encoding="utf8") as out_file:
            out_file.write(final_output)
        await status_message.reply_document(document="MissKatyEval.txt", caption=cmd[: 4096 // 4 - 1], disable_notification=True)
        os.remove("MissKatyEval.txt")
        await status_message.delete()
    else:
        await status_message.edit(final_output, parse_mode=enums.ParseMode.MARKDOWN)


async def aexec(code, client, message):
    exec("async def __aexec(client, message): " + "".join(f"\n {l_}" for l_ in code.split("\n")))
    return await locals()["__aexec"](client, message)


async def shell_exec(code, treat=True):
    process = await asyncio.create_subprocess_shell(code, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT)

    stdout = (await process.communicate())[0]
    if treat:
        stdout = stdout.decode().strip()
    return stdout, process.decode().strip()
