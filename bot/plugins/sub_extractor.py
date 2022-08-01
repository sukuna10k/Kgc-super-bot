from bot import app
from pyrogram import filters
from info import COMMAND_HANDLER
from bot.utils.decorator import capture_err
from bot.plugins.dev import shell_exec
import json
from time import perf_counter


@app.on_message(filters.command(["ceksub"], COMMAND_HANDLER))
@capture_err
async def ceksub(_, m):
    link = m.text.split(' ', 1)
    if len(link) == 1:
        return await m.reply(
            'Use command /ceksub [link] to check subtitle available in video.')
    start_time = perf_counter()
    pesan = await m.reply("Processing..")
    res = (await shell_exec(
        f"ffprobe -loglevel 0 -print_format json -show_format -show_streams {link}"
    ))[0]
    details = json.loads(res)
    DATA = []
    for stream in details["streams"]:
        mapping = stream['index']
        stream_name = stream['codec_name']
        stream_type = stream['codec_type']
        if stream_type in ("audio", "subtitle"):
            pass
        else:
            continue
        try:
            lang = stream["tags"]["language"]
        except:
            lang = mapping
        DATA.append({
            'mapping': mapping,
            'stream_name': stream_name,
            'stream_type': stream_type,
            'lang': lang
        })
    res = "".join(
        f"<b>Index:</b> {i['mapping']}\n<b>Stream Name:</b> {i['stream_name']}\n<b>Language:</b> {i['lang']}\n\n"
        for i in DATA)
    end_time = perf_counter()
    timelog = "{:.2f}".format(end_time - start_time) + " second"
    await pesan.edit(
        f"Daftar Sub & Audio File:\n{res}\n\nProcessed in {timelog}")
