using System;
using System.Threading.Tasks;
using Microsoft.Bot.Builder.Dialogs;
using Microsoft.Bot.Connector;
using System.Net.Http;
using System.Threading;
using System.Text.RegularExpressions;
using Newtonsoft.Json.Linq;

namespace Bot_Application4.Dialogs
{
    [Serializable]
    public class RootDialog : IDialog<object>
    {
        string kilometers;
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
                    kilometers = b;
                    await context.PostAsync($"Whats the address you want to start from?");
                    context.Wait(this.AddressAsync);
                }
            }

        }

        private async Task AddressAsync(IDialogContext context, IAwaitable<IMessageActivity> result)
        {
            var message = await result;
            var client = new HttpClient();
            var addr = message.Text;

            context.Wait(HelloAsync);
            var addr_enc = System.Uri.EscapeUriString(addr);
            var maplocal = await client.GetAsync("http://dev.virtualearth.net/REST/v1/Locations?q="+addr_enc+"&key=AlQARhB7rh_uKiu3fau3lFlxdGvQhGSsn-R_wD9XysMHF9ulHCYQIh_bY1ls_iRU");
            var links = await maplocal.Content.ReadAsStringAsync();

            var coords_txt = Regex.Matches(links, @"coordinates.:\[[0-9.-]*,[0-9.-]*\]}")[0].ToString();
            int length = coords_txt.Length;

            System.Diagnostics.Debug.WriteLine(length);

            // string s1 = coords_txt.Substring(14, length-1);

            //System.Diagnostics.Debug.WriteLine(s1);

            string lat = "";
            string lon = "";
            int i = 0;
            char current;
            
           // await context.PostAsync(current);
            do
            {
                if(i+1 >= length)
                {
                    break;
                }
                current = coords_txt[i];
                if ((Char.IsDigit(current) || current=='.'))
                {
                    lat += current;
                }
                
                i++;
            } while (current != ',');

            
            current = coords_txt[i];
            while(current != ']')
            {
                current = coords_txt[i];
                lon += current;
                i++;
            }
            lon = lon.Substring(0, lon.Length - 1);
            await context.PostAsync(lat);
            await context.PostAsync(lon);

            string site = "http://10.21.211.82:8000/maps/" + lon + "/" + lat + "/" + kilometers + "/True/5/";
            var ret = await client.GetAsync(site);
            var uri = await ret.Content.ReadAsStringAsync();
            var json = JObject.Parse(uri)["url"].ToString();
            await context.PostAsync(json);
            
            await context.PostAsync($"We generated a suitable route starting from {addr}!");
        }

    }
}
