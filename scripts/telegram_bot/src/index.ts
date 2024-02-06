import { Context, Telegraf } from 'telegraf'
import { Update } from 'telegraf/typings/core/types/typegram';
import { fetchUrlBySearchQuery } from './fetcher';

const BOT_TOKEN = "6676938301:AAHmBBV9d809u3TiWD3DorGk1QK4S1JoPJU";


const bot = new Telegraf(BOT_TOKEN);

const startBot = async () => {
	console.log("Bot running");
	bot.use((ctx) => {		
		const postJson = ctx.channelPost;
		const text = (postJson as any)?.text || "";
		if(text){ onNextText(text, ctx);}
	})
    
    await bot.launch(); //start the bot

    // Handling shutdowns gracefully
    process.once('SIGINT', () => bot.stop('SIGINT'));
    process.once('SIGTERM', () => bot.stop('SIGTERM'));

	console.log("Bot finished");
}

const onNextText = async (text: string, ctx: Context<Update>) => {
	const audioUrl = await fetchUrlBySearchQuery(text);
    const title = text;
    ctx.replyWithAudio(
        { url: audioUrl },
        { 
            title: "Dein Podcast",
            caption: title
        }
    );
	ctx.reply('Welcome ' + audioUrl)
}

startBot();


