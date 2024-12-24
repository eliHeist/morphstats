from django.views import View
from django.shortcuts import render
from django.db.models import Avg, Sum, Count, Max, Min, F
from django.utils.timezone import now
from Stat.models import Stat, Service


class StatisticsDashboardView(View):
    template_name = "dashboard/stats_dashboard.html"

    def get(self, request, *args, **kwargs):
        today = now().date()
        current_month = today.month
        current_year = today.year

        selected_month = int(request.GET.get('month', 0))
        selected_year = int(request.GET.get('year', 0))

        filtered_stats = self.get_filtered_stats(selected_year, selected_month, current_year, current_month)
        
        
        numbers_stats = {
            "morphers": self.calculate_stats(filtered_stats, 'totalAttendance'),
            "junior": self.calculate_stats(filtered_stats, 'totalJunior'),
            "senior": self.calculate_stats(filtered_stats, 'totalSenior'),
            "salvations": self.calculate_stats(filtered_stats, 'totalSalvations'),
            "first_time_visitors": self.calculate_stats(filtered_stats, 'totalVisitors'),
        }
        
        stats = {
            "facilitators_data": self.calculate_facilitators_served(filtered_stats),
        }
        

        stats["numbers_stats"] = []
        for key, value in numbers_stats.items():
            if key != "facilitators_served":
                stats["numbers_stats"].append({
                    "name": key.replace('_', ' ').capitalize(),
                    "highest": value["highest"],
                    "highest_stat": value["highest_stat"],
                    "lowest": value["lowest"],
                    "lowest_stat": value["lowest_stat"],
                    "average": value["average"],
                    "total": value["total"]
                })
        

        context = {"stats": stats}
        return render(request, self.template_name, context)

    def get_filtered_stats(self, selected_year, selected_month, current_year, current_month):
        if selected_year and not selected_month:
            return Stat.objects.filter(date__year=selected_year).prefetch_related('services')
        elif not selected_year and selected_month:
            return Stat.objects.filter(date__year=current_year, date__month=selected_month).prefetch_related('services')
        elif selected_year and selected_month:
            return Stat.objects.filter(date__year=selected_year, date__month=selected_month).prefetch_related('services')
        else:
            return Stat.objects.filter(date__year=current_year).prefetch_related('services')

    def calculate_stats(self, filtered_stats, method_name):
        total_stats = filtered_stats.count()
        stats = {"highest": 0, "lowest": float('inf'), "total": 0, "average": 0}

        for stat in filtered_stats:
            value = getattr(stat, method_name)()
            stats["total"] += value
            if value > stats["highest"]:
                stats["highest"] = value
                stats["highest_stat"] = stat
            if value < stats["lowest"]:
                stats["lowest"] = value
                stats["lowest_stat"] = stat

        if total_stats > 0:
            stats["average"] = round(stats["total"] / total_stats, 0)
        else:
            stats["lowest"] = 0

        return stats

    def calculate_facilitators_served(self, filtered_stats):
        data = {
            "total_sundays": filtered_stats.count(), #✔️
            "total_services": 0, #✔️
            "total_facilitation": 0, #--
            "average_facilitation": 0, #✔️
            "highest_facilitation": 0, #✔️
            "highest_facilitation_day": 0, #✔️
            "lowest_facilitation": 10000000, #✔️ # start at a high value to be able to get the lowest
            "lowest_facilitation_day": 0, #✔️
            "facilitators_dict": None,
            "total_facilitators": 0, #✔️
            "stats_list": [
                ['Date', 'Morphers', 'Facilitators']
            ]
        }
        facilitator_dict = {}

        for stat in filtered_stats:
            # increment total facilitation
            data["total_facilitation"] += stat.facilitatorsCount()
            data["stats_list"].append([stat.date.strftime("%d %b"), stat.totalAttendance(), stat.facilitatorsCount()])
            
            # find highest facilitation
            if stat.facilitatorsCount() > data["highest_facilitation"]:
                data["highest_facilitation"] = stat.facilitatorsCount()
                data["highest_facilitation_day"] = stat
            # find lowest facilitation
            if stat.facilitatorsCount() < data["lowest_facilitation"]:
                data["lowest_facilitation"] = stat.facilitatorsCount()
                data["lowest_facilitation_day"] = stat
            for service in stat.services.all():
                data["total_services"] += 1
                
                for facilitator in service.facilitators_available.all():
                    if facilitator not in facilitator_dict:
                        facilitator_dict[facilitator] = {"services_served": set(), "total_services_served": 0, "sundays_served": set(), "total_sundays_served": 0}
                    # set of services served
                    facilitator_dict[facilitator]["services_served"].add(service)
                    # number of services served
                    facilitator_dict[facilitator]["total_services_served"] = len(facilitator_dict[facilitator]["services_served"])
                    # set of sundays served
                    facilitator_dict[facilitator]["sundays_served"].add(stat)
                    # number of sundays served
                    facilitator_dict[facilitator]["total_sundays_served"] = len(facilitator_dict[facilitator]["sundays_served"])

        data["average_facilitation"] = round(data["total_facilitation"] / data["total_sundays"], 0)
        data["total_facilitators"] = len(facilitator_dict)

        sorted_facilitator_dict = dict( sorted(facilitator_dict.items(), key=lambda item: item[1]['total_sundays_served'], reverse=True) )
        
        data["facilitators_dict"] = sorted_facilitator_dict

        return data
