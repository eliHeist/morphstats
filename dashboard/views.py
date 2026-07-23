from django.views import View
from django.shortcuts import render
from django.utils import timezone
from Stat.models import Stat
from facilitators.models import Facilitator, GenderChoices


class StatisticsDashboardView(View):
    template_name = "dashboard/stats_dashboard.html"

    def get(self, request, *args, **kwargs):
        today = timezone.now().date()
        current_month = today.month
        current_year = today.year

        try:
            selected_month = int(request.GET.get('month', 0))
        except ValueError:
            selected_month = 0

        try:
            selected_year = int(request.GET.get('year', 0))
        except ValueError:
            selected_year = 0

        filtered_stats = self.get_filtered_stats(selected_year, selected_month, current_year, current_month)

        numbers_stats = {
            "attendance": self.calculate_stats(filtered_stats, 'totalAttendance'),
            "junior": self.calculate_stats(filtered_stats, 'totalJunior'),
            "senior": self.calculate_stats(filtered_stats, 'totalSenior'),
            "salvations": self.calculate_stats(filtered_stats, 'totalSalvations'),
            "first_time_visitors": self.calculate_stats(filtered_stats, 'totalVisitors'),
        }

        numbers_list = [
            {
                "name": key.replace('_', ' ').capitalize(),
                "highest": value["highest"],
                "highest_stat": value["highest_stat"],
                "lowest": value["lowest"],
                "lowest_stat": value["lowest_stat"],
                "daily_average": value["daily_average"],
                "total": value["total"],
            }
            for key, value in numbers_stats.items()
        ]

        stats = {
            "numbers_stats": numbers_list,
            "facilitators_data": self.calculate_facilitators_served(filtered_stats),
        }

        return render(request, self.template_name, {"stats": stats})

    def get_filtered_stats(self, selected_year, selected_month, current_year, current_month):
        # Prefetch tags along with facilitators to prevent N+1 queries in memory loops
        queryset = Stat.objects.prefetch_related(
            'services__facilitators_available__tags'
        )

        if selected_year and not selected_month:
            return queryset.filter(date__year=selected_year)
        elif not selected_year and selected_month:
            return queryset.filter(date__year=current_year, date__month=selected_month)
        elif selected_year and selected_month:
            return queryset.filter(date__year=selected_year, date__month=selected_month)
        else:
            return queryset.filter(date__year=current_year)

    def calculate_stats(self, filtered_stats, method_name):
        total_stats = len(filtered_stats)
        stats = {
            "highest": 0, "highest_stat": None,
            "lowest": float('inf'), "lowest_stat": None,
            "total": 0, "daily_average": 0,
        }

        if total_stats == 0:
            stats["lowest"] = 0
            return stats

        for stat in filtered_stats:
            value = getattr(stat, method_name)()
            stats["total"] += value

            if value >= stats["highest"]:
                stats["highest"] = value
                stats["highest_stat"] = stat

            if value <= stats["lowest"]:
                stats["lowest"] = value
                stats["lowest_stat"] = stat

        stats["daily_average"] = int(stats["total"] / total_stats) if total_stats > 0 else 0
        return stats

    def calculate_facilitators_served(self, filtered_stats):
        total_sundays = len(filtered_stats)
        total_active_pool = Facilitator.objects.filter(active=True).count()

        data = {
            "total_sundays": total_sundays,
            "total_services": 0,
            "total_facilitation": 0,
            "average_facilitation": 0,
            "highest_facilitation": 0,
            "highest_facilitation_day": None,
            "lowest_facilitation": 0 if total_sundays == 0 else float('inf'),
            "lowest_facilitation_day": None,
            "facilitators_dict": {},
            "total_facilitators": 0,
            "stats_list": [['Date', 'Morphers', 'Facilitators']],
            # New Statistics Keys
            "demographics": {
                "male_count": 0,
                "female_count": 0,
                "unspecified_count": 0,
                "engagement_rate": 0,
            },
            "tag_breakdown": {},
        }

        if total_sundays == 0:
            return data

        facilitator_dict = {}
        tag_counts = {}

        for stat in filtered_stats:
            services = list(stat.services.all())
            data["total_services"] += len(services)

            sunday_facilitators = set()
            for service in services:
                for facilitator in service.facilitators_available.all():
                    sunday_facilitators.add(facilitator)

                    if facilitator not in facilitator_dict:
                        facilitator_dict[facilitator] = {
                            "total_services_served": 0,
                            "sundays_served": set(),
                            "total_sundays_served": 0,
                        }
                    facilitator_dict[facilitator]["total_services_served"] += 1
                    facilitator_dict[facilitator]["sundays_served"].add(stat)

                    # Count Tag frequency
                    for tag in facilitator.tags.all():
                        tag_counts[tag.name] = tag_counts.get(tag.name, 0) + 1

            day_facilitators_count = len(sunday_facilitators)
            data["total_facilitation"] += day_facilitators_count

            data["stats_list"].append([
                stat.date.strftime("%d %b"),
                stat.totalAttendance(),
                day_facilitators_count,
            ])

            if day_facilitators_count >= data["highest_facilitation"]:
                data["highest_facilitation"] = day_facilitators_count
                data["highest_facilitation_day"] = stat

            if day_facilitators_count <= data["lowest_facilitation"]:
                data["lowest_facilitation"] = day_facilitators_count
                data["lowest_facilitation_day"] = stat

        # Process Facilitators Served stats & Demographics
        male_count = 0
        female_count = 0
        unspecified_count = 0

        for fac, f_data in facilitator_dict.items():
            f_data["total_sundays_served"] = len(f_data["sundays_served"])
            
            # Tally gender demographics
            if fac.gender == GenderChoices.MALE:
                male_count += 1
            elif fac.gender == GenderChoices.FEMALE:
                female_count += 1
            else:
                unspecified_count += 1

        # Summary Metrics
        data["average_facilitation"] = int(data["total_facilitation"] / total_sundays) if total_sundays > 0 else 0
        data["total_facilitators"] = len(facilitator_dict)
        
        # Demographics payload
        data["demographics"]["male_count"] = male_count
        data["demographics"]["female_count"] = female_count
        data["demographics"]["unspecified_count"] = unspecified_count
        data["demographics"]["engagement_rate"] = (
            round((len(facilitator_dict) / total_active_pool) * 100, 1) if total_active_pool > 0 else 0
        )
        data["tag_breakdown"] = tag_counts

        # Sort facilitators by most Sundays served
        data["facilitators_dict"] = dict(
            sorted(
                facilitator_dict.items(),
                key=lambda item: item[1]['total_sundays_served'],
                reverse=True
            )
        )

        return data

