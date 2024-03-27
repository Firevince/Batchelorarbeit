import { Context, Telegraf } from 'telegraf'
import { Update } from 'telegraf/typings/core/types/typegram';
import { fetchUrlBySearchQuery } from './fetcher';
import { config } from './config';

const bot = new Telegraf(config.BOT_TOKEN);

const startBot = async () => {
	console.log("Bot running");
	bot.use((ctx) => {		
		const text = (ctx.update as any).message.text;
		if(text){ onNextText(text, ctx);}
	})
    
    await bot.launch(); //start the bot

    // Handling shutdowns gracefully
    process.once('SIGINT', () => bot.stop('SIGINT'));
    process.once('SIGTERM', () => bot.stop('SIGTERM'));

	console.log("Bot finished");
}

const onNextText = async (text: string, ctx: Context<Update>) => {
	console.log("searching " + text)
	const audioUrl = await fetchUrlBySearchQuery(text);
    const title = text;
    ctx.replyWithAudio(
        { url: audioUrl },
        { 
            title: title,
            caption: title
        }
    );
}

startBot();


