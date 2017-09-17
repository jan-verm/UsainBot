using System;
using System.Threading.Tasks;
using Microsoft.Bot.Builder.Dialogs;
using Microsoft.Bot.Connector;
using System.Net.Http;
using System.Threading;

namespace Bot_Application4.Dialogs
{
    [Serializable]
    public class RootDialog : IDialog<object>
    {
        public Task StartAsync(IDialogContext context)
        {
            context.Wait(HelloAsync);

            return Task.CompletedTask;
        }

        private async Task HelloAsync(IDialogContext context, IAwaitable<IMessageActivity> result)
        {
            var message = await result;

            if (message.Text.ToLower().Contains("hello") || message.Text.ToLower().Contains("hi")) {
                await context.PostAsync($"Greetings to you as well, would you like to go on a run?");
                context.Wait(this.WantToRunAsync);
            }
        }

        private async Task WantToRunAsync(IDialogContext context, IAwaitable<IMessageActivity> result)
        {
            var message = await result;

            if (message.Text.ToLower().Contains("yes"))
            {
                await context.PostAsync($"How many kilometers you want to run?");
                context.Wait(this.KilometersAsync);
            }
        }

        private async Task KilometersAsync(IDialogContext context, IAwaitable<IMessageActivity> result)
        {
            var message = await result;

            if (message.Text.ToLower().Contains("km") || message.Text.ToLower().Contains("kilometers"))
            {
                string b = string.Empty;

                for (int i = 0; i < message.Text.Length; i++)
                {
                    if (Char.IsDigit(message.Text[i]))
                        b += message.Text[i];
                }
                if (b.Length > 0)
                {
                    await context.PostAsync($"Whats the address you want to start from?");
                    context.Wait(this.AddressAsync);
                }
            }

        }

        private async Task AddressAsync(IDialogContext context, IAwaitable<IMessageActivity> result)
        {
            var message = await result;

            var addr = message.Text;

            context.Wait(HelloAsync);

            await context.PostAsync($"We'll generate a suited route starting from {addr}!");
        }







        // calculate something for us to return
        //  int length = (activity.Text ?? string.Empty).Length;
        //Stuff added by Parth
        //int kilos = (activity.Text ?? string.Empty).Kilos;
        //Parth Stopped here
        //var client = new HttpClient();

        //client.DefaultRequestHeaders.Add("Ocp-Apim-Subscription-Key", "AlQARhB7rh_uKiu3fau3lFlxdGvQhGSsn - R_wD9XysMHF9ulHCYQIh_bY1ls_iRU"); 
        // return our reply to the user
        // string length =  
        //Parth Started here

        /*
        if(activity.Text == "yes")
        {
            await context.Forward(new SecondDialog(), this.ResumeAfterSecondDialog, "hello", CancellationToken.None);
        }

        string kilometers = "";
        string a = activity.Text;
        string b = string.Empty;

        for (int i = 0; i < a.Length; i++)
        {
            if (Char.IsDigit(a[i]))
                b += a[i];
        }
        if (b.Length>0)
        {
            kilometers = b;
            await context.PostAsync(text: $"So you want to run {kilometers} km?");
        }

        else if(activity.Text.Contains("Yes i do"))
        {

            await context.PostAsync($"You sent {activity.Text}. Want to go for a run?");

        var resultt = await client.GetAsync("http://10.21.211.82/example_link.html");

        var geojsonlink = await resultt.Content.ReadAsStringAsync();
        await context.PostAsync(text: $"We did it here it is {geojsonlink} ");
        context.Wait(MessageReceivedAsync);
        }*/

    }
}